"""
ASGI config for base project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter , URLRouter
from chat.consumers import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http" : get_asgi_application() , 
        "websocket" : AuthMiddlewareStack(
            URLRouter(
                # routing.websocket_urlpatterns
                path("ws/chat/", ChatConsumer.as_asgi())
            )    
        )
    }
)