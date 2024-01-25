from django.urls import path
from . import views


urlpatterns = [
    path('cache/',views.PostView.as_view(), name='cache'),

        ]
