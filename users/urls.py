from django.urls import path
from . import views
from django.contrib.auth import views as authViews


# Отслеживаются адреса, начинающиеся на 'user/'
urlpatterns = [
    # Работа с пользователем - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    path('reg/', views.register, name="reg"),
    path('profile/', views.profile, name='profile'),
    # path('', authViews.
    path('', authViews.LoginView.as_view(template_name='users/user.html'), name='user'),
    path('exit/', authViews.LogoutView.as_view(template_name='users/exit.html'), name='exit'),
    # Восстановление пароля - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    path('pass-reset/', authViews.PasswordResetView.as_view(template_name='users/pass_reset.html'), name='pass-reset'),
    path('password_reset_complete/', authViews.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('password_reset_confirm/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_done/', authViews.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
]
