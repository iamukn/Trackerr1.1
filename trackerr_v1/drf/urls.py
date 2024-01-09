from django.urls import path
from .views import views, APIView, genView

urlpatterns = [
    path('gen/', genView.GenView.as_view(), name='gen' ),
    path('list/', APIView.ListView.as_view(), name='list' ),
    path('home/', views.home, name='home' ),

        ]
