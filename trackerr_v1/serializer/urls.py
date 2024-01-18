from django.urls import path
from . import views 


urlpatterns = [
    path('people/', views.PersonView.as_view(), name='people'),
        ]

