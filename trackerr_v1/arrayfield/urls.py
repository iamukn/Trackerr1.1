from django.urls import path
from . import views
urlpatterns = [
    path('array/',views.arrView.as_view(), name='array' ),
        ]
