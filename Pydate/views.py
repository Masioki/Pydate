from datetime import date

from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
from .utils.personality_test import get_personality_type
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout

from Pydate import settings
from Pydate.forms import RegisterForm, PersonalQuestionsForm
from Pydate.models import PersonalityTestItem, PersonalityTestAnswer, UserData, PersonalQuestionUser, \
    PersonalQuestionContent, PersonalQuestionAnswer, Match
from django.forms import formset_factory
from django.contrib.auth.models import User


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def base(request):
    if request.user.is_authenticated:
        return render(request, 'html_pages/view_people.html', {})
    return render(request, 'html_pages/base.html', {})


# W register.html wystarczy wstawić {{form}} albo samemu rozłożyć
# za pomocą notacji {{ }} {% %}
@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            profile = UserData(user=user)
            profile.birth = form.cleaned_data.get('birth_date')
            profile.sex = form.cleaned_data.get('sex')
            profile.searching_for = form.cleaned_data.get('searching_for')
            profile.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            first_item_id = PersonalityTestItem.objects.order_by('itemID')[0].itemID
            context = {'first_item_id': first_item_id}
            return render(request, 'html_pages/personality_test.html', context)
    else:
        form = RegisterForm()
    return render(request, 'html_pages/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return redirect('html_pages/login.html')
    return render(request, 'html_pages/login')


def personality_test(request):
    first_item_id = PersonalityTestItem.objects.order_by('itemID')[0].itemID
    context = {'first_item_id': first_item_id}
    return render(request, 'html_pages/personality_test.html', context)


def test_vote(request, test_item_id):
    test_item = get_object_or_404(PersonalityTestItem, pk=test_item_id)
    if request.method == "POST":
        ans, creation = PersonalityTestAnswer.objects.get_or_create(itemID=test_item, user=request.user)
        try:
            ans.answer = request.POST['choice']
            ans.save()
        except (KeyError, MultiValueDictKeyError):
            return render(request, 'html_pages/test_choice.html',
                          {'test_item': test_item, 'error_message': "You didn't select a choice!"})

        if PersonalityTestItem.objects.filter(pk=test_item_id + 1).exists():
            next_test_item = PersonalityTestItem.objects.get(pk=test_item_id + 1)
            return render(request, 'html_pages/test_choice.html', {'test_item': next_test_item})
        else:
            user = UserData.objects.get(user_id=request.user.id)
            user.personality = get_personality_type(user.user.id)
            user.save()
            return render(request, 'html_pages/test_summary.html')
    else:
        return render(request, 'html_pages/test_choice.html', {'test_item': test_item})


def logout_view(request):
    logout(request)
    return render(request, 'html_pages/base.html', {})


@login_required
def personal_questionnaire(request, username):
    question_user = User.objects.get(username=username)
    match = Match.objects.filter(user1=request.user, user2=question_user)
    if not match:
        match = Match.objects.filter(user1=question_user, user2=request.user)
        if not match:
            return redirect("/")
        # question_user = request.user  # to replace with the upper line
    question_user = request.user  # to replace with the upper line
    questions = []
    questions_ids = []
    personal_questions_user = PersonalQuestionUser.objects.filter(user=question_user)
    if personal_questions_user:
        for p in personal_questions_user:
            answer = PersonalQuestionAnswer.objects.filter(user=request.user)
            if answer:
                return redirect('/')
            queryset = PersonalQuestionContent.objects.filter(questionID=str(p.id)).values("content").all()
            if queryset:
                questions += [q["content"] for q in queryset]
                questions_ids.append(str(p.id))
    formset_form = formset_factory(PersonalQuestionsForm, extra=len(questions_ids))
    if request.method == "POST":
        formset = formset_form(request.POST)
        if formset.is_valid():
            for i, form in enumerate(formset):
                if form.is_valid():
                    answer = form.save(commit=False)
                    answer.user = request.user
                    answer.questionID = PersonalQuestionContent.objects.get(pk=i + 1)
                    answer.save()
            return redirect('/')
    else:
        formset = formset_form()
    return render(request, 'html_pages/personal_questionnaire.html', {"formset": formset, "questions": questions})


@login_required
def my_matches(request):
    matches_data = []
    # search matches for user1=request.user
    matches = Match.objects.filter(user1=request.user)
    if matches:
        for match in matches:
            if match.personal_questions_match == "11":
                u = UserData.objects.get(user=match.user2)
                # matches_data.append({"username": u.user.username, "description": u.description, "photo": u.photo})
                matches_data.append({"username": u.user.username, "description": u.description})
    # search matches for user2=request.user
    matches = Match.objects.filter(user2=request.user)
    if matches:
        for match in matches:
            if match.personal_questions_match == "11":
                u = UserData.objects.get(user=match.user1)
                # matches_data.append({"username": u.user.username, "description": u.description, "photo": u.photo})
                matches_data.append({"username": u.user.username, "description": u.description})
    if len(matches_data) == 0:
        display_no_matches_info = True
    else:
        info = ""
        display_no_matches_info = False

    return render(request, 'html_pages/my_matches.html',
                  {"matches_data": matches_data, "display_no_matches_info": display_no_matches_info})


@login_required
def view_answers(request):
    # tu elementu ktore zwroce
    questions = []
    descriptions = []
    photos = []
    users_ids = []
    users_index = []
    ages = []
    question_content = []
    # tu juz nie
    personal_questions_user = PersonalQuestionUser.objects.filter(user=request.user)

    if personal_questions_user:
        for p in personal_questions_user:
            answerset = PersonalQuestionAnswer.objects.filter(questionID=str(p.id))
            questionset = PersonalQuestionContent.objects.filter(questionID=str(p.id)).values("content").all()
            if answerset:
                for usr in answerset:
                    if str(usr.user) not in users_ids:
                        questions += [[str(usr.content)]]
                        users_ids += [(str(usr.user))]
                        question_content += [[q["content"] for q in questionset]]
                        # sets
                        userset = UserData.objects.filter(user=str(usr.user.id)).values("id", "description", "photo",
                                                                                        "birth").all()
                        userset2 = UserData.objects.filter(user=str(usr.user.id)).values("user_id").all()
                        # data from sets
                        descriptions += [' ' + q["description"] for q in userset]
                        photos += [q["photo"] for q in userset]
                        ages += [calculate_age(q["birth"]) for q in userset]
                        users_index += [(q["user_id"]) for q in userset2]
                    else:
                        for idu, u in enumerate(users_ids):
                            if (str(usr.user) == u):
                                questions[idu] += [(str(usr.content))]
                                question_content[idu] += [q["content"] for q in questionset]

    formset_form = formset_factory(PersonalQuestionsForm, extra=len(users_ids))

    formset = formset_form()
    return render(request, 'html_pages/view_answers.html',
                  {"formset": formset, "question_content": question_content, "names": users_ids,
                   "user_index": users_index, "descriptions": descriptions, "questions": questions, "age": ages,
                   "img": photos, 'media_url': settings.STATIC_URL})


def questions_delete(us1, us2):
    # usuwanie pytan
    personal_questions_user = PersonalQuestionUser.objects.filter(user=us1)
    if personal_questions_user:
        for ques in personal_questions_user:
            PersonalQuestionAnswer.objects.filter(user=us2, questionID=ques.questionID).delete()


def match_delete(request, user_id=None):
    comrade = User.objects.get(id=str(user_id))
    # usuwanie matchow
    Match.objects.filter(user1=request.user, user2=comrade).delete()
    Match.objects.filter(user1=comrade, user2=request.user).delete()

    questions_delete(request.user, comrade)  # usuwam odpowiedzi comrade'a na pytania zalogowanego uzytkownika
    questions_delete(comrade, request.user)  # a tu vice versa
    return redirect("view_answers")


def match_accept(request, user_id=None):
    comrade = User.objects.get(id=str(user_id))
    match = Match.objects.filter(user1=request.user, user2=comrade)
    if match:
        if len(match) > 1:
            return HttpResponseNotFound(
                '<h1>Error. W bazie sa 2 takie same matche. Skontaktuj sie z administracja</h1>')
        m = match[0]
        if (m.personal_questions_match == Match.Agreement.AGREE_2_TO_1):
            m.personal_questions_match = Match.Agreement.AGREE_BOTH
        else:
            m.personal_questions_match = Match.Agreement.AGREE_1_TO_2
        m.save()
    else:
        match = Match.objects.filter(user2=request.user, user1=comrade)
        if len(match) > 1:
            return HttpResponseNotFound(
                '<h1>Error. W bazie sa 2 takie same matche. Skontaktuj sie z administracja</h1>')
        if match:
            m = match[0]
            if (m.personal_questions_match == Match.Agreement.AGREE_1_TO_2):
                m.personal_questions_match = Match.Agreement.AGREE_BOTH
            else:
                m.personal_questions_match = Match.Agreement.AGREE_2_TO_1
            m.save()
        else:
            return HttpResponseNotFound('<h1>Error. W bazie nie ma danego matcha. Skontaktuj sie z administracja</h1>')

    questions_delete(request.user, comrade)  # usuwam odpowiedzi comrade'a na pytania zalogowanego uzytkownika
    return redirect("view_answers")
