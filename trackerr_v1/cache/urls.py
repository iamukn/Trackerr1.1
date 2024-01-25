from django.urls import path
from . import views


urlpatterns = [
    path('cache/',views.PostView.as_view(), name='cache'),
    path('caches/',views.PaginateView.as_view(), name='caches'),

        ]
