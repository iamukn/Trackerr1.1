#!/usr/bin/python3
""" handles routing for the trackerr backend """

from authentication.views.auth import CustomTokenObtainPairView as TokenObtain
#from authentication.views.auth import CustomTokenBlacklistView as Blacklist
from rest_framework_simplejwt.views import TokenBlacklistView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from shared.swagger import schema_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/', include('user.urls')),
    path('api/v1/', include('business.urls')),
    path('api/v1/', include('logistics.routes')),
    path('api/v1/', include('tracking_information.urls')),
    path('api/v1/auth/token/', TokenObtain.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('api/v1/swagger/', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
