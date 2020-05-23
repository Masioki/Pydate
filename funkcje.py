import sqlite3
import random

import django
import os
from datetime import date
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pydate.settings')
django.setup()

from Pydate.models import PersonalQuestionUser, PersonalQuestionContent, User, UserData, Match


def dodaj_pytanie():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("INSERT INTO starter_question ('content') VALUES ('pytam')")
    conn.commit()
    conn.close()
# dodaj_pytanie()


def populate():
    for a in range(8):
        user = User(username=str(a), password="helloworld")
        user.save()
        profile = UserData(user=user)
        profile.birth = date.today()
        profile.sex = "F"
        profile.searching_for = "M"
        profile.description = "esfbhfssbef"
        profile.save()
    for a in range(10):
            p1 = PersonalQuestionContent(content="How are you?")
            p1.save()
            user = User.objects.all()[0]
            p2 = PersonalQuestionUser(user=user, questionID=p1)
            p2.save()
    for a in range(3):
        numbers = [i for i in range(8)]
        user1_rn = numbers[random.randint(0, len(numbers) - 1)]
        numbers.remove(user1_rn)
        user2_rn = numbers[random.randint(0, len(numbers) - 1)]
        numbers.remove(user2_rn)
        user1 = User.objects.get(username=user1_rn)
        user2 = User.objects.get(username=user2_rn)
        if a == 0:
            chat = Match(user1=user1, user2=user2, personal_questions_match="00")
        elif a == 1:
            chat = Match(user1=user1, user2=user2, personal_questions_match="01")
        else:
            chat = Match(user1=user1, user2=user2, personal_questions_match="11")
        chat.save()

if __name__ == "__main__":
    populate()
