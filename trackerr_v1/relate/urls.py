from django.urls import path
from . import views as relate_view

app = 'relate'

urlpatterns = [
    path('unique/',relate_view.Unique.as_view(), name='unique' ),
    path('home/',relate_view.Home.as_view(), name='home' ),

        ]
