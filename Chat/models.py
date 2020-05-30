from channels.db import database_sync_to_async
from django.db import models
from Pydate.models import UserData


class Chat(models.Model):
    chatID = models.IntegerField(primary_key=True)
    agreement = models.IntegerField(default=0)


class UserChat(models.Model):
    chatID = models.ForeignKey(Chat, on_delete=models.CASCADE)
    userID = models.ForeignKey(UserData, on_delete=models.CASCADE)

    @staticmethod
    def user_belongs_to(user, chat_id):
        # TODO: sprawdź czy użytkownik przynależy do danego czatu
        return True

    @staticmethod
    @database_sync_to_async
    def get_available_chats(user):
        # TODO
        return []


class ChatMessage(models.Model):
    chatID = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)

    # TODO: brakuje kto wysłał

    # zapisujemy bez niepotrzebnych spacji
    def save(self, *args, **kwargs):
        self.message = self.message.strip()
        super(ChatMessage, self).save(*args, **kwargs)

    @staticmethod
    def get_latest(chat_id, start, end):
        # TODO: wyciągnij wiadomości z range(start,end), np. range(0,10) oznacza 10 najnowszych wiadomości
        return []
