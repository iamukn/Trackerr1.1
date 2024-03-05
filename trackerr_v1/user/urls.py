from django.urls import path
from .views import (
    views,
    users_count,
    password_recovery,
    change_password
)


urlpatterns = [
    path('users/', views.UsersView.as_view(), name='users'),
    path('user/<int:pk>/', views.UserView.as_view(), name='user'),
    path('users-count/',users_count.Users_count.as_view(), name='users-count'),
    path('reset-password/',password_recovery.Recover_password.as_view(), name='recovery'),
    path('change-password/', change_password.ChangePassword.as_view(), name='change-password'),
        ]
