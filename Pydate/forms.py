
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#
class RegisterForm(UserCreationForm):
    # TODO: dodatkowe pola do User

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)  # TODO: Wszystkie pola
