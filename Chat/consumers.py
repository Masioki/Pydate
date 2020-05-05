from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
import json
from django.core.serializers.json import DjangoJSONEncoder
from twisted.protocols.memcache import ClientError

from Chat.models import UserChat, ChatMessage


class ChatConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.available_chats = []
        self.open_chats = []

    async def connect(self):
        user = self.scope["user"]
        self.available_chats = await UserChat.get_available_chats(user)
        self.available_chats.append(1)  # TODO: Usunąć, to tylko dla testu
        if user.is_anonymous:
            await self.close()
        else:
            await self.accept()

    async def receive_json(self, content, **kwargs):
        command = content["type"]
        if command == "JOIN":
            await self.join_chat(content["chat_id"])
        elif command == "LEAVE":
            await self.leave_chat(content["chat_id"])
        elif command == "MESSAGE":
            await self.send_chat(content["chat_id"], content["message"])

    async def disconnect(self, code):
        for chat_id in self.open_chats:
            await self.leave_chat(chat_id)

    async def join_chat(self, chat_id):
        # refresh
        if chat_id not in self.available_chats:
            self.available_chats = await UserChat.get_available_chats(self.scope["user"])
        if chat_id in self.available_chats:
            await self.channel_layer.group_add(
                str(chat_id),
                self.channel_name,
            )
            self.open_chats.append(chat_id)
        else:
            raise ClientError("Cannot join chat")

    async def leave_chat(self, chat_id):
        self.open_chats.remove(chat_id)
        await self.channel_layer.group_discard(
            str(chat_id),
            self.channel_name,
        )

    async def send_chat(self, chat_id, message):
        if chat_id not in self.open_chats:
            raise ClientError("Access denied")
        await self.channel_layer.group_send(
            str(chat_id),
            {
                "type": "chat_message",
                "chat_id": chat_id,
                "username": self.scope["user"].first_name,
                "message": message,
            }
        )

    async def chat_message(self, event):
        print(event["message"])
        chat_id = event["chat_id"]
        username = event["username"]
        message = event["message"]
        date = json.dumps(await ChatMessage.save_message(username, chat_id, message), cls=DjangoJSONEncoder)
        await self.send_json(
            {
                "type": "MESSAGE",
                "chat_id": chat_id,
                "username": username,
                "message": message,
                "date": date
            },
        )
