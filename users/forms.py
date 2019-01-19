from django.forms import EmailField, CharField, CheckboxInput, BooleanField, HiddenInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.forms import ModelForm, Form

from .models import CustomUser


class CustomPasswordForm(PasswordChangeForm):
    """ Inherits from Django's default password form change and disables autofocus"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields['old_password'].widget.attrs)
        self.fields['old_password'].widget.attrs.update({'autofocus': False})


class PreferencesForm(ModelForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email')


class LoginForm(AuthenticationForm):
    remember_me = BooleanField(
        required=False, widget=CheckboxInput(), label="Remember me")


class RegisterForm(UserCreationForm):
    email = EmailField()

    first_name = CharField(max_length=30, required=False, help_text='Optional.')
    last_name = CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password1',
            'password2'
        ]
