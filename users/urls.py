from django.contrib.auth.views import PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy

from users import views
from users.views import RegisterView, ProfileView, RegisterDoneView, RegisterConfirmView, UserPasswordResetView, \
    CustomLoginView

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register_done/', RegisterDoneView.as_view(), name='register_done'),
    path('register_confirm/<uidb64>/<token>/', RegisterConfirmView.as_view(), name="register_confirm"),
    path('profile/<email>', ProfileView.as_view(), name='profile'),
    path('password-reset/',
         UserPasswordResetView.as_view(
             template_name="users/password_reset_form.html",
             email_template_name="users/password_reset_email.html",
             success_url=reverse_lazy("users:password_reset_done")
         ),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html",
                                          success_url=reverse_lazy("users:password_reset_complete")
                                          ),
         name='password_reset_confirm'
         ),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name='password_reset_complete'
         ),
]
