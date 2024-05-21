import secrets

from django.contrib.auth import login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, LoginView
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserRegisterForm, UserProfileForm, CustomLoginForm
from users.models import User
from users.servises import activate_email_task, activate_new_password_task


class CustomLoginView(LoginView):
    model = User
    authentication_form = CustomLoginForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация на сайте'}

    def form_valid(self, form):
        valid = super().form_valid(form)
        email, password = form.cleaned_data.get('username'), form.cleaned_data.get('password') # username==email!!!
        user = User.objects.get(email=email)
        if user.is_blocked:
            raise ValidationError("Этот аккаунт заблокирован. Обратитесь к администратору.")
        login(self.request, user)
        return valid

    def get_success_url(self):
        return reverse_lazy('main:home')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user: User = form.save()
        user.is_active = False
        user.save()
        activate_email_task(user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("users:register_done")


class RegisterDoneView(TemplateView):
    template_name = "users/register_done.html"
    extra_context = {"title": "Регистрация завершена, активируйте учётную запись."}


class RegisterConfirmView(View):
    @staticmethod
    def get(request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return render(
                request,
                "users/register_confirmed.html",
                {"title": "Учётная запись активирована."},
            )
        else:
            return render(
                request,
                "users/register_not_confirmed.html",
                {"title": "Ошибка активации учётной записи."},
            )


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('main:home')

    def get_object(self, queryset=None):
        return User.objects.get(email=self.kwargs.get("email"))


class UserPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'users/password_reset_form.html'
    success_url = reverse_lazy('users:login')
    code = secrets.token_hex(8)

    def form_valid(self, form):
        if self.request.method == 'POST':
            email = self.request.POST['email']
            try:
                user = User.objects.filter(email=email).first()
                password = UserPasswordResetView.code
                user.set_password(password)
                user.save()
                activate_new_password_task(user, password)
                return HttpResponseRedirect(reverse('users:login'))
            except (Exception):
                return self.render_to_response('users:register')

        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('/') # на главную страницу сайта


def user_is_blocked_view(request):
    if request.user.is_blocked:
        logout(request)
    return render(request,'users/user_is_blocked.html')
