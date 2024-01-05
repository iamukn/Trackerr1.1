from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Track

router = DefaultRouter()
router.register('tracking', Track, basename='tracking')


urlpatterns = [
    path('', include(router.urls)),

        ]
