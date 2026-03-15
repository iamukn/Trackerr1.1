"""
ASGI config for trackerr_v1 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

django_asgi_app = get_asgi_application()

from .middleware import JWTAuthMiddleware
import tracking_information.routing
import logistics.wsgi_routes

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trackerr_v1.settings")

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter(
            tracking_information.routing.websocket_urlpatterns +  # handles WebSocket URLs
            logistics.wsgi_routes.websocket_urlpatterns,
        )
    ),
})

