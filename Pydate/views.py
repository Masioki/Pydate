import json
import urllib.request
from datetime import date
from math import radians, cos, sin, asin, sqrt

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db.models import Q
from django.dispatch import receiver
from django.forms import formset_factory
from django.http import JsonResponse
from django.http.response import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_http_methods

from Chat.models import UserChat
from Pydate import settings
from Pydate.forms import RegisterForm, PersonalQuestionsForm
from Pydate.models import PersonalityTestItem, PersonalityTestAnswer
from Pydate.models import UserData, PersonalQuestionUser, PersonalQuestionContent, PersonalQuestionAnswer, Match, \
    UserLog
from funkcje import choose_best_by_personality
from .utils.personality_test import get_personality_type


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


@login_required
@require_http_methods(["POST"])
def update_profile_picture(request):
    file = request.FILES.get('image')
    user = request.user
    user = UserData.objects.get(user=user)
    user.photo = file
    user.save()
    return JsonResponse({'message': 'success'}, status=200)


@login_required
@require_http_methods(["POST"])
def update_profile(request):
    user = request.user
    if user.check_password(request.POST['password']):
        data = request.POST
        user_data = UserData.objects.filter(user=user)[0]
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        user_data.sex = data['sex']
        user_data.birth = data['birth']
        user_data.description = data['description']
        user_data.searching_for = data['looking_for']
        user.save()
        user_data.save()
        return JsonResponse({'message': 'success'}, status=200)
    else:
        return JsonResponse({'message': 'Wrong password!'}, status=400)


@login_required
@require_http_methods(["GET"])
def profile(request):
    user = request.user
    user_data = UserData.objects.filter(user=user)[0]
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'birth': user_data.birth,
        'description': user_data.description,
        'sex': user_data.sex,
        'looking_for': user_data.searching_for,
        'img': user_data.photo
    }
    return render(request, 'html_pages/profile_editor.html', {'data': data})


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
            prof = UserData(user=user)
            prof.birth = form.cleaned_data.get('birth_date')
            prof.sex = form.cleaned_data.get('sex')
            prof.searching_for = form.cleaned_data.get('searching_for')
            prof.save()
            log = UserLog(user=user)
            log.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            first_item_id = PersonalityTestItem.objects.order_by('itemID')[0].itemID
            context = {'first_item_id': first_item_id}
            return render(request, 'html_pages/personality_test.html', context)
    else:
        form = RegisterForm()
    return render(request, 'html_pages/register.html', {'form': form})


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#
#         else:
#             return redirect('html_pages/login.html')
#     return render(request, 'html_pages/login')

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


def info_view(request):
    return render(request, 'html_pages/view_info.html', {})


@login_required
def personal_questionnaire(request, username):
    question_user = User.objects.get(username=username)
    match = Match.objects.filter(user1=request.user, user2=question_user)
    if not match:
        match = Match.objects.filter(user1=question_user, user2=request.user)
        if not match:
            return redirect("/")
        # question_user = request.user  # to replace with the upper line
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
            if match.chatting_match == "11":
                u = UserData.objects.get(user=match.user2)
                # matches_data.append({"username": u.user.username, "description": u.description, "photo": u.photo})
                matches_data.append({"username": u.user.username, "description": u.description})
    # search matches for user2=request.user
    matches = Match.objects.filter(user2=request.user)
    if matches:
        for match in matches:
            if match.chatting_match == "11":
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
    locations = []
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
                        # lokalizacja
                        locations += [float("{0:.2f}".format(distance_between(usr.user, request.user)))]

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
                            if str(usr.user) == u:
                                questions[idu] += [(str(usr.content))]
                                question_content[idu] += [q["content"] for q in questionset]

    formset_form = formset_factory(PersonalQuestionsForm, extra=len(users_ids))

    formset = formset_form()
    return render(request, 'html_pages/view_answers.html',
                  {"formset": formset, "question_content": question_content, "names": users_ids,
                   "user_index": users_index, "descriptions": descriptions, "questions": questions, "age": ages,
                   "img": photos, "local": locations, 'media_url': settings.STATIC_URL})


def questions_delete(us1, us2):
    # usuwanie pytan
    personal_questions_user = PersonalQuestionUser.objects.filter(user=us1)
    if personal_questions_user:
        for ques in personal_questions_user:
            PersonalQuestionAnswer.objects.filter(user=us2, questionID=ques.questionID).delete()


def match_decline(user1, id):
    comrade = User.objects.get(id=str(id))
    # zmiana matchow na AGREE_NONE
    match = Match.objects.filter(user1=user1, user2=comrade)
    if match:
        match[0].chatting_match = Match.Agreement.AGREE_NONE
        return
    else:
        match = Match.objects.filter(user2=user1, user1=comrade)
        if match:
            match[0].chatting_match = Match.Agreement.AGREE_NONE
            return

    # Jesli nie bylo matcha to go robie i ustawaim na AGREE_NONE
    if match:
        match.save()
    else:
        if user1.username < comrade.username:
            match = Match.objects.create(user1=user1, user2=comrade, chatting_match=Match.Agreement.AGREE_1_TO_2)
        else:
            match = Match.objects.create(user2=user1, user1=comrade, chatting_match=Match.Agreement.AGREE_2_TO_1)
        match.save()

    questions_delete(user1, comrade)  # usuwam odpowiedzi comrade'a na pytania zalogowanego uzytkownika
    questions_delete(comrade, user1)  # a tu vice versa


def match_delete(request, id=None):
    match_decline(request.user, id)
    return redirect("view_answers")


def match_accept(request, id=None):
    comrade = User.objects.get(id=str(id))
    match = Match.objects.filter(user1=request.user, user2=comrade)
    if match:
        if len(match) > 1:
            return HttpResponseNotFound(
                '<h1>Error. W bazie sa 2 takie same matche. Skontaktuj sie z administracja</h1>')
        m = match[0]
        if m.personal_questions_match == Match.Agreement.AGREE_2_TO_1:
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
            if m.personal_questions_match == Match.Agreement.AGREE_1_TO_2:
                m.personal_questions_match = Match.Agreement.AGREE_BOTH
            else:
                m.personal_questions_match = Match.Agreement.AGREE_2_TO_1
            m.save()
        else:
            return HttpResponseNotFound('<h1>Error. W bazie nie ma danego matcha. Skontaktuj sie z administracja</h1>')

    questions_delete(request.user, comrade)  # usuwam odpowiedzi comrade'a na pytania zalogowanego uzytkownika
    return redirect("view_answers")


"""Elementy wykorzystane do strony glownej"""

"""pomocnicze"""


def select_comrade_for_me(suspect):
    available_users = []
    try:
        suspect_data = UserData.objects.get(user=suspect)
    except:
        return suspect
    users_data = UserData.objects.filter(sex=suspect_data.searching_for, searching_for=suspect_data.sex).all()
    for u in users_data:
        match = Match.objects.filter(
            Q(
                Q(user1=suspect, user2=u.user),
                ~Q(chatting_match=Match.Agreement.AGREE_2_TO_1)
            ) |
            Q(
                Q(user1=u.user, user2=suspect),
                ~Q(chatting_match=Match.Agreement.AGREE_1_TO_2)
            )
        )
        if not match:
            available_users.append(u.user)
    # TODO TUTAJ WSTAW LISTE OD NAJATRAKCUJNIEJSZYSZ DO NAJMNIEJ ATRAKCYJNYCH.
    # JESLI bedzie TA OSOBA W available_users to ja zwroc, jak nie to sprawdz nastepna najlepsza mozliwa osobe
    if len(available_users) == 0:
        return suspect
    else:
        return choose_best_by_personality(suspect.profile.personality, available_users)


def create_match(us1, us2):  # najpierw requested potem towarzysz
    if us1.username < us2.username:
        match = Match.objects.create(user1=us1, user2=us2, chatting_match=Match.Agreement.AGREE_1_TO_2)
    else:
        match = Match.objects.create(user2=us1, user1=us2, chatting_match=Match.Agreement.AGREE_2_TO_1)
    match.save()


"""glawne"""


@login_required
def view_people(request):
    age = description = location = photo = ''
    user = request.user
    chats = UserChat.chats_info(user)
    candidate = select_comrade_for_me(request.user)
    userid = candidate.id
    if request.user == candidate:
        display = False
    else:
        display = True
        candidate_info = UserData.objects.filter(user=candidate)

        for u in candidate_info:
            description = u.description
            photo = u.photo
            age = calculate_age(u.birth)
            location = float("{0:.2f}".format(distance_between(candidate, request.user)))
    return render(request, 'html_pages/view_people.html',
                  {'chats': chats, 'username': user.username, "desc": description, "age": age, "loc": location,
                   "nick": candidate, "name": userid, "photo": photo,
                   "display": display, 'media_url': settings.STATIC_URL})


def yes_crush(request, id=None):
    comrade = User.objects.get(id=str(id))
    "statystyka"
    log_com = UserLog.objects.get(user=comrade)
    log_my = UserLog.objects.get(user=request.user)
    log_com.likes_receive += 1
    log_my.likes_sent += 1
    log_com.save()
    log_my.save()
    "koniec staystyki"

    match = Match.objects.filter(user1=request.user, user2=comrade)
    if match:
        if len(match) > 1:
            return HttpResponseNotFound(
                '<h1>Error. W bazie sa 2 takie same matche. Skontaktuj sie z administracja</h1>')
        m = match[0]
        if m.chatting_match == Match.Agreement.AGREE_2_TO_1:
            m.chatting_match = Match.Agreement.AGREE_BOTH
        else:
            m.chatting_match = Match.Agreement.AGREE_1_TO_2
        m.save()
    else:
        match = Match.objects.filter(user2=request.user, user1=comrade)
        if len(match) > 1:
            return HttpResponseNotFound(
                '<h1>Error. W bazie sa 2 takie same matche. Skontaktuj sie z administracja</h1>')
        if match:
            m = match[0]
            if m.chatting_match == Match.Agreement.AGREE_1_TO_2:
                m.chatting_match = Match.Agreement.AGREE_BOTH
            else:
                m.chatting_match = Match.Agreement.AGREE_2_TO_1
            m.save()
        else:
            create_match(request.user, comrade)

    return redirect("view_people")


def no_crush(request, id=None):
    match_decline(request.user, id)
    return redirect("view_people")


"""Lokalizacja"""


@receiver(user_logged_in)
def update_geolocation(sender, user, request, *args, **kwargs):
    try:
        usr = UserData.objects.get(user=user)
    except UserData.DoesNotExist:
        print("\nError, wyczysc baze userow i zarejestruj ich od nowa\n")
        return
    ip = get_client_ip(request)
    x = urllib.request.urlopen('http://ip-api.com/json/' + ip + '?fields=lat,lon')
    data = x.read()
    js = json.loads(data.decode('utf-8'))
    try:
        usr.latitude = js['lat']
        usr.longitude = js['lon']
        usr.save()
    except KeyError:
        usr.latitude = 0
        usr.longitude = 0
        usr.save()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def distance_between(usr1, usr2):
    user1 = UserData.objects.get(user=usr1)
    user2 = UserData.objects.get(user=usr2)
    lat1, lon1, lat2, lon2 = map(radians, [user1.latitude, user1.longitude, user2.latitude, user2.longitude])
    d_lat = lat1 - lat2
    d_lon = lon1 - lon2
    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2  # Haversine formula
    c = 2 * asin((sqrt(a)))
    R = 6371
    return c * R  # w km


"koniec lokalizacji"
