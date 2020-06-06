from channels.db import database_sync_to_async
from django.contrib.auth.models import User
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models


class Chat(models.Model):
    chatID = models.AutoField(primary_key=True, default=0)
    agreement = models.IntegerField(default=0)


# TODO: do użytkownika nie chatu

class UserChat(models.Model):
    userChatID = models.AutoField(primary_key=True, unique=True, default=0)
    chatID = models.ForeignKey(Chat, unique=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User,unique=False, on_delete=models.CASCADE)

    @staticmethod
    def user_belongs_to(user, chat_id):
        return UserChat.objects.filter(chatID=chat_id, user=user)

    @staticmethod
    @database_sync_to_async
    def get_available_chats(user):
        return [i.chatID.chatID for i in list(UserChat.objects.filter(user=user))]

    @staticmethod
    def chats_info(user):
        result = []
        for i in list(UserChat.objects.filter(user=user)):
            temp = {
                "chat_id": i.chatID.chatID,
                "username": list(UserChat.objects.filter(chatID=i.chatID.chatID).exclude(user=user))[0].user.username
            }
            result.append(temp)
        return result


class ChatMessage(models.Model):
    messageID = models.AutoField(primary_key=True, default=0)
    chat = models.ForeignKey(Chat, unique=False, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now=True, unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # zapisujemy bez niepotrzebnych spacji
    def save(self, *args, **kwargs):
        self.message = self.message.strip()
        super(ChatMessage, self).save(*args, **kwargs)

    @staticmethod
    @database_sync_to_async
    def save_message(username, chat_id, message):
        user = list(User.objects.filter(username=username))[0]
        chat = Chat.objects.get(chatID=chat_id)
        mes = ChatMessage(user=user, chat=chat, message=message)
        mes.save()
        return mes.date

    @staticmethod
    def get_latest(chat_id, start, end):
        chat = Chat.objects.get(chatID=chat_id)
        mes_list = list(ChatMessage.objects.filter(chat=chat).order_by('-date'))
        end = min(max(end, 0), len(mes_list))
        start = max(start, 0)
        mes_list = mes_list[start:end]
        json_list = []
        for i in mes_list[::-1]:
            temp = {
                "type": "MESSAGE",
                "chat_id": i.chat.chatID,
                "username": i.user.username,
                "message": i.message,
                "date": json.dumps(i.date, cls=DjangoJSONEncoder)
            }
            json_list.append(temp)
        return json_list
