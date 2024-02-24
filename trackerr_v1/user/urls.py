from django.urls import path
from .views import views


urlpatterns = [
    path('users/', views.UsersView.as_view(), name='users'),
    path('user/<int:pk>/', views.UserView.as_view(), name='user'),
    path('users-count/',views.Users_count.as_view(), name='users-count'),
        ]
