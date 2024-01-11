from django.urls import path, include
from .views import views, APIView, genView, viewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('new-list', viewset.UserViewSet, basename='viewset')

urlpatterns = [
    path('', include(router.urls)),
    path('gen/', genView.GenView.as_view(), name='gen' ),
    path('list/', APIView.ListView.as_view(), name='list' ),
    path('home/', views.home, name='home' ),

        ]
