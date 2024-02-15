from django.urls import path
from . import views


urlpatterns = [
    path('users/', views.UsersView.as_view(), name='users'),
        ]
