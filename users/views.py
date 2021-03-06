from django.contrib.messages.views import SuccessMessageMixin
from users.forms import RegisterForm, LoginForm, PreferencesForm, CustomPasswordForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate

from .models import CustomUser as User

from django.shortcuts import render, redirect

from django.contrib.auth import update_session_auth_hash

# Tokens
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

from django.contrib.auth.forms import PasswordChangeForm
from braces.views import FormMessagesMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.base import TemplateView  # new


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    redirect_field_name = 'login'


class PreferencesView(LoginRequiredMixin, FormView):
    template_name = 'cbv_multiple_forms.html'

    def get(self, request, *args, **kwargs):
        preferences_form = PreferencesForm(
            instance=self.request.user, prefix="preferences")
        password_form = CustomPasswordForm(self.request.user)

        return render(
            self.request,
            template_name=self.template_name,
            context={
                'preferences_form': preferences_form,
                'password_form': password_form
            })

    def post(self, request, *args, **kwargs):
        print("self.request.POST", self.request.POST)
        print("self.request.POST.get('preferences') == 'password'",
              self.request.POST.get('preferences') == 'password')

        preferences_form = PreferencesForm()
        password_form = PasswordChangeForm(request.user)

        if request.POST.get("preferences") == 'preferences':
            preferences_form = PreferencesForm(
                self.request.POST,
                instance=self.request.user,
                prefix="preferences")

            if preferences_form.is_valid():
                print("preferences form is valid")

                preferences_form.save()
                messages.info(request, "User info Updated")
                return redirect('preferences')

        if request.POST.get("preferences") == 'password':
            password_form = PasswordChangeForm(
                request.user, request.POST, prefix="password")

            if password_form.is_valid():
                print("password form is valid")
                print("self.request.user", self.request.user)

                user = password_form.save()

                update_session_auth_hash(request, user)  # Important!

                messages.info(request, "Password changed")
                return redirect('preferences')

        return render(
            self.request,
            template_name=self.template_name,
            context={
                'preferences_form': preferences_form,
                'password_form': password_form
            })


class LoginView(FormMessagesMixin, FormView):
    """ Extended Login view with remember me functionality """

    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')
    form_invalid_message = "Username or password invalid. Please try again"
    form_valid_message = "Logged in successfully"

    def form_valid(self, form):
        login(self.request, form.get_user())

        if not form.cleaned_data.get('remember_me'):
            self.request.session.set_expiry(0)

        return super(LoginView, self).form_valid(form)


class RegisterView(SuccessMessageMixin, CreateView):
    """ Extended Register View with custom Registration form and able to send emails"""
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'
    success_message = "Registered successfully"

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        current_site = get_current_site(self.request)
        subject = 'Activate Your MySite Account'
        message = render_to_string(
            'email_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
        user.email_user(subject, message)

        return redirect('home')


from django.views import View


class SendEmailVerification(LoginRequiredMixin, View):

    def get(self, request):
        current_site = get_current_site(self.request)
        subject = 'Verify your email'
        message = render_to_string(
            'email_activation.html', {
                'user': self.request.user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(self.request.user.pk)
                                            ).decode(),
                'token': account_activation_token.make_token(self.request.user),
            })
        self.request.user.email_user(subject, message)
        messages.info(
            request,
            "A verification email has been sent to the email address specified")
        return redirect('preferences')


from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login
from django.contrib import messages


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        messages.success(request, "Your email has been verified")
        return redirect('home')
    else:
        messages.warning(request, "Your email address could not be verified")
        return redirect('home')
