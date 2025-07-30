import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import BallotBlaze.real_time_update.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BallotBlaze_Server.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            BallotBlaze.real_time_update.routing.websocket_urlpatterns
        )
    ),
})