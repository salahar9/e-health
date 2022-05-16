"""
ASGI config for ehealth project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
import django
from decouple import config
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f'{config("PROJECT_NAME")}.settings')
django.setup()
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import notifications.routing
import django_chatter.routing





application = ProtocolTypeRouter({
    
    "websocket": AuthMiddlewareStack(
        URLRouter(
            notifications.routing.websocket_urlpatterns,
            django_chatter.routing.websocket_urlpatterns # send request to chatter's urls

        )
    )
    # Just HTTP for now. (We can add other protocols later.)
})