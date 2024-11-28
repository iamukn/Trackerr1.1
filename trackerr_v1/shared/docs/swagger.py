from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

""" Swagger Schema """

schema_view = get_schema_view(
   openapi.Info(
      title="Trackerr API",
      default_version='v1',
      description="Simplified documentation for the trackerr API",
      terms_of_service="https://trackerr.live/terms/",
      contact=openapi.Contact(email="n.u.kingsley@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
