from django.forms import EmailField, CharField, CheckboxInput, BooleanField, HiddenInput
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.forms import ModelForm, Form


from .models import CustomUser

class CustomPasswordForm(PasswordChangeForm):
    """ Inherits from Django's default password form change and disables autofocus"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields['old_password'].widget.attrs)
        self.fields['old_password'].widget.attrs.update({'autofocus': False})

        # self.fields['comment'].widget.attrs.update(size='40')


# class PasswordForm(Form):
#     current_password = CharField(max_length=150)
#     new_password = CharField(max_length=150)


class PreferencesForm(ModelForm):
    # password = CharField(widget=PasswordInput())
    # action = CharField(max_length=60, widget=HiddenInput())

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name','last_name', 'email')

from django.contrib.auth.forms import UserChangeForm
# from django.contrib.auth.models import User

# class PreferencesForm(UserChangeForm):
#     def __init__(self, *args, **kwargs):
#         super(PreferencesForm, self).__init__(*args, **kwargs)
#         del self.fields['password']
#
#     class Meta:
#         model = User
#         fields = ('username','email','first_name','last_name')
#

#######################################################################################
# # Approach here https://www.codementor.io/lakshminp/handling-multiple-forms-on-the-same-page-in-django-fv89t2s3j
#
# class MultipleForm(Form):
#     action = CharField(max_length=60, widget=HiddenInput())
#
#
# class PasswordForm(Form):
#     current_password = CharField(max_length=150)
#     new_password = CharField(max_length=150)
#
# class UserInfoForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email')

###############################################################################

# class PreferencesForm(MultiModelForm):
#     form_classes = {
#         'user_form': UserInfoForm,
#         'password_form': PasswordForm,
#     }


class LoginForm(AuthenticationForm):
    remember_me = BooleanField(required=False, widget=CheckboxInput(), label="Remember me")


class RegisterForm(UserCreationForm):
    email = EmailField()

    first_name = CharField(max_length=30, required=False, help_text='Optional.')
    last_name = CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
