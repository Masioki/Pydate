from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout
from Pydate.forms import RegisterForm, PersonalQuestionsForm
from Pydate.models import UserData, PersonalQuestionUser, PersonalQuestionContent, PersonalQuestionAnswer
from django.forms import formset_factory


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
        'looking_for': user_data.searching_for
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
                    answer.questionID = PersonalQuestionContent.objects.get(pk=i + 1)
                    answer.save()
            return redirect('/')
    else:
        formset = formset_form()
    return render(request, 'html_pages/personal_questionnaire.html', {"formset": formset, "questions": questions})
