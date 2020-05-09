from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import render, redirect
from Chat.models import UserChat, ChatMessage


@login_required
def index(request, chat_id):
    user = request.user
    if UserChat.user_belongs_to(user, chat_id):
        messages = ChatMessage.get_latest(chat_id, 0, 20)
        # print(serializers.serialize('json', messages))
        # TODO: mapowanie modelu wiadomości do odpowiedniego JSON-a
        content = {
            'chat_id': chat_id,
            'messages': serializers.serialize('json', messages),
            'username': user.username
        }
        return render(request, 'index.html', content)
    else:
        return redirect('/')
