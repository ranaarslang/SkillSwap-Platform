import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close(code=4401)
            return
        self.peer_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_group_name = f"chat_{min(self.scope['user'].id, int(self.peer_id))}_{max(self.scope['user'].id, int(self.peer_id))}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name); await self.accept()
    async def disconnect(self, close_code): await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    async def receive(self, text_data):
        body = json.loads(text_data).get("body", "").strip()
        if not body: return
        await self.save_message(body)
        await self.channel_layer.group_send(self.room_group_name, {"type": "chat.message", "body": body, "sender": self.scope["user"].username})
    async def chat_message(self, event): await self.send(text_data=json.dumps({"body": event["body"], "sender": event["sender"]}))
    @database_sync_to_async
    def save_message(self, body): Message.objects.create(sender=self.scope["user"], recipient_id=self.peer_id, body=body)
