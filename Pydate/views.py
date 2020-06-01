from datetime import date

import json
import urllib

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout

from Pydate import settings
from Pydate.forms import RegisterForm, PersonalQuestionsForm
from Pydate.models import UserData, PersonalQuestionUser, PersonalQuestionContent, PersonalQuestionAnswer,Match
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
            update_geolocation(request, user)
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
            update_geolocation(request, user)
        else:
            return redirect('html_pages/login.html')
    return render(request, 'html_pages/login')


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
                    answer.questionID = PersonalQuestionContent.objects.get(pk=i+1)
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
#tu elementu ktore zwroce
    questions = []
    descriptions=[]
    photos=[]
    users_ids=[]
    users_index=[]
    ages=[]
    question_content = []
#tu juz nie
    personal_questions_user = PersonalQuestionUser.objects.filter(user=request.user)

    if personal_questions_user:
        for p in personal_questions_user:
            answerset = PersonalQuestionAnswer.objects.filter(questionID=str(p.id))
            questionset = PersonalQuestionContent.objects.filter(questionID=str(p.id)).values("content").all()
            if answerset:
                for usr in answerset:
                    if (str(usr.user) not in users_ids):
                        questions += [[str(usr.content)]]
                        users_ids+=[(str(usr.user))]
                        question_content+=[[q["content"] for q in questionset]]
                        #sets
                        userset = UserData.objects.filter(user=str(usr.user.id)).values("id","description","photo","birth").all()
                        userset2 = UserData.objects.filter(user=str(usr.user.id)).values("user_id").all()
                        #data from sets
                        descriptions += [' '+q["description"] for q in userset]
                        photos += [q["photo"] for q in userset]
                        ages+= [calculate_age(q["birth"]) for q in userset]
                        users_index+= [(q["user_id"]) for q in userset2]
                    else:
                        for idu, u in enumerate(users_ids):
                            if(str(usr.user) == u):
                                questions[idu]+=[(str(usr.content))]
                                question_content[idu] += [q["content"] for q in questionset]

    formset_form = formset_factory(PersonalQuestionsForm, extra=len(users_ids))

    formset = formset_form()
    return render(request, 'html_pages/view_answers.html', {"formset": formset, "question_content":question_content,"names":users_ids,"user_index":users_index, "descriptions": descriptions,"questions": questions,"age": ages, "img":photos, 'media_url': settings.STATIC_URL})

def questions_delete(us1, us2):
    #usuwanie pytan
    personal_questions_user = PersonalQuestionUser.objects.filter(user=us1)
    if personal_questions_user:
        for ques in personal_questions_user:
            PersonalQuestionAnswer.objects.filter( user=us2,questionID=ques.questionID).delete()

def match_delete(request, id=None):
    comrade = User.objects.get(id=str(id))
    #usuwanie matchow
    Match.objects.filter(user1=request.user, user2=comrade).delete()
    Match.objects.filter(user1=comrade, user2=request.user).delete()

    questions_delete(request.user, comrade)#usuwam odpowiedzi comrade'a na pytania zalogowanego uzytkownika
    questions_delete(comrade,request.user )#a tu vice versa
    return redirect("view_answers")

def match_accept(request, id=None):
    comrade = User.objects.get(id=str(id))
    match=Match.objects.filter(user1=request.user, user2=comrade)
    if match:
        if (len(match) > 1):
            return HttpResponseNotFound('<h1>Error. W bazie sa 2 takie same matche. Skontaktuj sie z administracja</h1>')
        m = match[0]
        if (m.personal_questions_match == Match.Agreement.AGREE_2_TO_1):
            m.personal_questions_match = Match.Agreement.AGREE_BOTH
        else:
            m.personal_questions_match=Match.Agreement.AGREE_1_TO_2
        m.save()
    else:
        match = Match.objects.filter(user2=request.user, user1=comrade)
        if(len(match)>1):
            return HttpResponseNotFound('<h1>Error. W bazie sa 2 takie same matche. Skontaktuj sie z administracja</h1>')
        if match:
            m = match[0]
            if(m.personal_questions_match == Match.Agreement.AGREE_1_TO_2):
                m.personal_questions_match = Match.Agreement.AGREE_BOTH
            else:
                m.personal_questions_match = Match.Agreement.AGREE_2_TO_1
            m.save()
        else:
            return HttpResponseNotFound('<h1>Error. W bazie nie ma danego matcha. Skontaktuj sie z administracja</h1>')

    questions_delete(request.user, comrade)#usuwam odpowiedzi comrade'a na pytania zalogowanego uzytkownika
    return redirect("view_answers")


def update_geolocation(request, user):
    ip = get_client_ip(request)
    x = urllib.request.urlopen('http://ip-api.com/json/' + ip + '?fields=lat,lon')
    data = x.read()
    js = json.loads(data.decode('utf-8'))
    try:
        user.latitude = js['lat']
        user.longitude = js['lon']
    except KeyError:
        user.latitude = 0
        user.longitude = 0

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip