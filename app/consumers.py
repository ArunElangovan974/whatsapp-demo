import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.other_user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_name = f"chat_{min(self.user.id, self.other_user_id)}_{max(self.user.id, self.other_user_id)}"
        
        if self.user.is_authenticated:
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        receiver = await sync_to_async(User.objects.get)(id=self.other_user_id)
        new_message = await sync_to_async(Message.objects.create)(
            sender=self.user, receiver=receiver, content=message
        )

        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": self.user.username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))
