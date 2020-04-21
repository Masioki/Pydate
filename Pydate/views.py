from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .forms import RegisterForm


def base(request):
    return render(request, 'html_pages/base.html', {})


# W register.html wystarczy wstawić {{form}} albo samemu rozłożyć
# za pomocą notacji {{ }} {% %}
@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form.save()
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'html_pages/register.html', {'form': form})
