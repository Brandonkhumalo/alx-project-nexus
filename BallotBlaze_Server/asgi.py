import os
import django 
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BallotBlaze_Server.settings')
django.setup()
import BallotBlaze.real_time_update.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            BallotBlaze.real_time_update.routing.websocket_urlpatterns
        )
    ),
})

'''$env:DJANGO_SETTINGS_MODULE="BallotBlaze_Server.settings"
daphne BallotBlaze_Server.asgi:application'''
#daphne -b 0.0.0.0 -p 8000 BallotBlaze_Server.asgi:application