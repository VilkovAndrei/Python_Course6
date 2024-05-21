from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


from users.models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'phone', 'avatar', 'comment')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class CustomLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['email', 'password']
