from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    chatID = models.AutoField(primary_key=True)
    agreement = models.IntegerField(default=0)


class UserChat(models.Model):
    chatID = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @staticmethod
    def user_belongs_to(user, chat_id):
        return UserChat.objects.filter(chatID=chat_id, user=user)

    @staticmethod
    @database_sync_to_async
    def get_available_chats(user):
        return list(UserChat.objects.filter(user=user))


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, unique=False, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now=True)
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
        return []
        # chat = Chat.objects.get(chatID=chat_id)
        # return list(ChatMessage.objects.filter(chat=chat).order_by('date'))[start:end]
