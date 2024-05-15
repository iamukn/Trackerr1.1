"""
URL configuration for trackerr_v1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from rest_framework.schemas import get_schema_view

from authentication.views.auth import CustomTokenObtainPairView as TokenObtain
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
            TokenObtainPairView,
                TokenRefreshView,
                )
from shared.swagger import schema_view



urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/', include('user.urls')),
    path('api/v1/', include('business.urls')),
    path('api/v1/', include('logistics.routes')),
    path('api/v1/', include('tracking_information.urls')),
    path('api/v1/token/', TokenObtain.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/swagger/', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
