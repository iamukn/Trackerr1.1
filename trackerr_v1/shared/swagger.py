#!/usr/bin/env python3

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

""" Swagger UI View and setting up the metadata """

schema_view = get_schema_view(
    openapi.Info(
        title="Trackerr_ API",
        default_version='v1',
        description="Backend API for the Trackerr application",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="n.u.kingsley@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
