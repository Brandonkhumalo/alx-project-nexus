import json
from channels.generic.websocket import AsyncWebsocketConsumer
from ..models import PollOption
from ..serializers.pollSerializer import PollOptionSerializer

class PollResultConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.poll_id = self.scope['url_route']['kwargs']['poll_id']
        self.room_group_name = f'poll_{self.poll_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def poll_update(self, event):
        await self.send(text_data=json.dumps(event['data']))