from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
from .utils.personality_test import get_personality_type
from .models import personality_test_item, personality_test_answer, user_data
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout
from Pydate.forms import RegisterForm, PersonalQuestionsForm
from Pydate.models import UserData, PersonalQuestionUser, PersonalQuestionContent, PersonalQuestionAnswer
from django.forms import formset_factory

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
            return redirect('/')
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
    first_item_id = personality_test_item.objects.order_by('itemID')[0].itemID
    context = {'first_item_id': first_item_id}
    return render(request, 'html_pages/personality_test.html', context)


def test_vote(request, test_item_id):
    test_item = get_object_or_404(personality_test_item, pk=test_item_id)
    if request.method == "POST":
        ans, creation = personality_test_answer.objects.get_or_create(itemID=test_item, user=request.user)
        try:
            ans.answer = request.POST['choice']
            ans.save()
        except (KeyError, MultiValueDictKeyError):
            return render(request, 'html_pages/test_choice.html', {'test_item': test_item, 'error_message': "You didn't select a choice!"})

        if personality_test_item.objects.filter(pk=test_item_id+1).exists():
            next_test_item = personality_test_item.objects.get(pk=test_item_id+1)
            return render(request, 'html_pages/test_choice.html', {'test_item': next_test_item})
        else:
            user = user_data.objects.get(pk=request.user.id)
            user.personality = get_personality_type(user.userID)
            user.save()
            return render(request, 'html_pages/test_summary.html')
    else:
        return render(request, 'html_pages/test_choice.html', {'test_item': test_item})

def logout_view(request):
    logout(request)
    return render(request, 'html_pages/base.html', {})


@login_required
def personal_questionnaire(request):
    # question_user = request.question_user / data
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
                    answer.questionID = PersonalQuestionContent.objects.get(pk=i+1)
                    answer.save()
            return redirect('/')
    else:
        formset = formset_form()
    return render(request, 'html_pages/personal_questionnaire.html', {"formset": formset, "questions": questions})
