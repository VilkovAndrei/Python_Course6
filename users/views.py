import secrets

from django.contrib.auth import login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, LoginView
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
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
        global USER_IS_MANAGER
        valid = super().form_valid(form)
        email, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')  # username==email!!!
        user = User.objects.get(email=email)
        if user.is_blocked:
            raise ValidationError("Этот аккаунт заблокирован. Обратитесь к администратору.")
        login(self.request, user)
        # print(f"'mailing_manager' - {user.groups.filter(name='mailing_manager').exists()}")
        if user.groups.filter(name='mailing_manager').exists():
            user.is_manager = True
        #     pass
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


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'users/user_list.html'
    extra_context = {'title': "Пользователи сервиса"}
    permission_required = 'users.set_user_is_blocked'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailing_manager'] = self.request.user.groups.filter(name='mailing_manager').exists()

        context_data['object_list'] = User.objects.all()
        return context_data


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
            except Exception:
                return self.render_to_response('users:register')

        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('/')  # на главную страницу сайта


def blocked_user(request, pk):
    """Блокирует или снимает блокировку с пользователя"""
    user_item = get_object_or_404(User, pk=pk)
    if request.user.is_staff and user_item.is_superuser:
        return HttpResponse("Невозможно заблокировать суперпользователя.", status=403)
    if not user_item.is_blocked:
        user_item.is_blocked = True
    elif user_item.is_blocked:
        user_item.is_blocked = False
    user_item.save()
    return redirect(reverse('users:user_list'))
