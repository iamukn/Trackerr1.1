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
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from oneToOne import views as one_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title = 'API trackerr',
        default_version='v1',
        description = 'Test',
        ),
    public = True,
    permission_classes = [permissions.AllowAny]
        )



urlpatterns = (
    path('swag/', schema_view.with_ui('swagger', cache_timeout=0), name='schema_swagger_ui'),
    path("admin/", admin.site.urls),
    path('drf/', include('drf.urls')),
    path('', include('books.urls')),
    path('', include('tracking.urls')),
    path('api/', include('serializer.urls')),
    path('', include('cache.urls')),
    path('docs/', include_docs_urls(title='TrackerrAPI')),
    path('', include('oneToOne.route')),
    path('', include('relate.urls')),
#    path(
#        "trackerr/",
#        get_schema_view(
#            title="Trackerr official schema", description="API for all things in trackerr", version="1.0.0"
#        ),
#        name="Trackerrapi-schema",
#    ),
)
