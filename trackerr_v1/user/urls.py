from django.urls import path
from .views import views, users_count


urlpatterns = [
    path('users/', views.UsersView.as_view(), name='users'),
    path('user/<int:pk>/', views.UserView.as_view(), name='user'),
    path('users-count/',users_count.Users_count.as_view(), name='users-count'),
        ]
