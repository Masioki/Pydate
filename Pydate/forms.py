import datetime
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from Pydate.models import User
from Pydate.models import PersonalQuestionAnswer
from django import forms


class RegisterForm(UserCreationForm):
    initial_date = datetime.date.today() - datetime.timedelta(days=365*18)
    birth_date = forms.DateField(initial=initial_date)
    username = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=200)
    sex = forms.ChoiceField(choices=(("F", "F"), ("M", "M")))
    searching_for = forms.ChoiceField(choices=(("F", "F"), ("M", "M"), ("Both", "Both")))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'birth_date', 'sex', 'searching_for')

    def clean_birth_date(self):
        data = self.cleaned_data['birth_date']
        if data > datetime.date.today() - datetime.timedelta(days=365*18):
            raise ValidationError(_('You have to be an adult to create a profile!'))
        return data


class PersonalQuestionsForm(ModelForm):
    answer_to_question = forms.CharField(required=True,
                                         widget=forms.TextInput(attrs={"class": "answer", "required": "true"}),
                                         max_length=200)

    class Meta:
        model = PersonalQuestionAnswer
        fields = ("answer_to_question",)

    def clean_answer_to_question(self):
        answer = self.cleaned_data['answer_to_question']
        if not answer or answer == "":
            print("HALO TU")
            raise ValidationError("Please, answer all of the questions")
        return answer

