import os
from django.core.asgi import get_asgi_application
from coquus.routing import application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coquus.settings')

django_application = get_asgi_application()


def application(scope):
    if scope['type'] == 'http':
        # If the connection is HTTP, use Django's ASGI application
        return django_application
    elif scope['type'] == 'websocket':
        # If the connection is WebSocket, use the routing configuration
        return application(scope)
