from django.urls import path
from . import views as relate_view

app = 'relate'

urlpatterns = [
    path('home/',relate_view.Home.as_view(), name='home' )

        ]
