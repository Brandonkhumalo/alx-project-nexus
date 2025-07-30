from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/polls/(?P<poll_id>\d+)/$', consumers.PollResultConsumer.as_asgi()),
]

#ws://localhost:8000/ws/polls/<poll_id>/