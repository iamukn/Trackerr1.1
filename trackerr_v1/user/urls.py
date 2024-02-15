from django.urls import path
from . import views


urlpatterns = [
    path('users/', views.UsersView.as_view(), name='users'),
    path('user/<int:pk>/', views.UserView.as_view(), name='user'),
        ]
