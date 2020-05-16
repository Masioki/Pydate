from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout

from Pydate import settings
from Pydate.forms import RegisterForm, PersonalQuestionsForm
from Pydate.models import UserData, PersonalQuestionUser, PersonalQuestionContent, PersonalQuestionAnswer
from django.forms import formset_factory
from django.contrib.auth.models import User


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

@login_required
def view_answers(request):
    # question_user = request.question_user / data
    question_user = request.user  # to replace with the upper line
    questions = []
    users=[]
    #tu pod usera rzeczy
    ages=[]
    descriptions=[]
    photos=[]
    names=[]
    users_ids=[]
    answer_ids=[]
    #tu juz nie
    questions_ids = []
    i=0
    personal_questions_user = PersonalQuestionUser.objects.filter(user=request.user)
    if personal_questions_user:
        for p in personal_questions_user:
            answerset = PersonalQuestionAnswer.objects.filter(questionID=str(p.id)).values("content").all()
            usersset = PersonalQuestionAnswer.objects.filter(questionID=str(p.id)).values("user")
            idsset = PersonalQuestionAnswer.objects.filter(questionID=str(p.id)).values("id").all()

            if answerset:
                questions += [q["content"] for q in answerset]
                answer_ids += [q["id"] for q in idsset]
                questions_ids.append(str(p.id))
                users_ids+=[q["user"] for q in usersset]
                desset = UserData.objects.filter(user=(users_ids[i])).values("description").all()
                nameset = User.objects.filter(id=(users_ids[i])).values("username").all()
                picset = UserData.objects.filter(user=(users_ids[i])).values("photo").all()
                descriptions += [q["description"] for q in desset]
                names += [q["username"] for q in nameset]
                photos += [q["photo"] for q in picset]
                i+=1

    """
    for i in range(len(users_ids)) :
        desset= UserData.objects.filter(id=str(users_ids[i])).values("description").all()
        nameset= User.objects.filter(id=str(users_ids[i])).values("username").all()
        picset= UserData.objects.filter(id=str(users_ids[i])).values("photo").all()
        descriptions+= [q["description"] for q in desset]
        names+= [q["username"] for q in nameset]
        photos+=[q["photo"] for q in picset]
    """



    formset_form = formset_factory(PersonalQuestionsForm, extra=len(questions_ids))

    if request.method == "POST":
        formset = formset_form(request.POST)
    else:
        formset = formset_form()
    return render(request, 'html_pages/view_answers.html', {"formset": formset, "question_id":answer_ids,"names":names, "descriptions": descriptions,"questions": questions,"img":photos, 'media_url': settings.STATIC_URL})

def question_delete(request, id=None):
   instance = get_object_or_404(PersonalQuestionAnswer, id=id)
   instance.delete()
   return redirect("view_answers")
