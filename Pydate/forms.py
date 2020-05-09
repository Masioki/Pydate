import datetime

from django.contrib.auth.forms import UserCreationForm
from Pydate.models import User
from django import forms


class RegisterForm(UserCreationForm):
    birth_date = forms.DateField(initial=datetime.date.today)
    username = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=200)
    facebook = forms.CharField(max_length=100)
    instagram = forms.CharField(max_length=100)
    sex = forms.ChoiceField(choices=((1, ("F")), (2, ("M"))))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'birth_date', 'facebook', 'instagram', 'sex')
