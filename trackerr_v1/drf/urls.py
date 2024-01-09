from django.urls import path
from .views import views, APIView

urlpatterns = [
    path('list/', APIView.ListView.as_view(), name='list' ),
    path('home/', views.home, name='home' ),

        ]
