from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode

from users.models import User


class SendEmail:
    def __init__(self, user: User):
        self.user = user
        self.current_site = Site.objects.get_current().domain
        self.token = default_token_generator.make_token(self.user)
        self.uid = urlsafe_base64_encode(str(self.user.pk).encode())

    def send_activate_email(self):
        reset_password_url = reverse_lazy("users:register_confirm", kwargs={"uidb64": self.uid, "token": self.token})
        subject = f"Активация аккаунта на сайте {self.current_site}"
        message = (
            f"Благодарим за регистрацию на сайте {self.current_site}.\n"
            "Для активации учётной записи, пожалуйста перейдите по ссылке:\n"
            f"http://{self.current_site}{reset_password_url}\n"
        )

        self.user.send_confirm_email(subject=subject, message=message)

    def send_password_reset(self, new_password):
        subject = f"Сброс пароля на сайте {self.current_site}"
        message = (
            f"Для авторизации на сайте используйте новый пароль:{new_password}\n"
        )

        self.user.send_confirm_email(subject=subject, message=message)


def activate_email_task(user: User):
    send_email = SendEmail(user=user)
    send_email.send_activate_email()


def activate_new_password_task(user: User, password):
    send_email = SendEmail(user=user)
    send_email.send_password_reset(password)
