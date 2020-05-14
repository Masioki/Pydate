import sqlite3
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pydate.settings')
django.setup()

from Pydate.models import PersonalQuestionUser, PersonalQuestionContent, User


def dodaj_pytanie():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("INSERT INTO starter_question ('content') VALUES ('pytam')")
    conn.commit()
    conn.close()
# dodaj_pytanie()


def populate():
    for a in range(10):
            p1 = PersonalQuestionContent(content="How are you?")
            p1.save()
            user = User.objects.all()[0]
            p2 = PersonalQuestionUser(user=user, questionID=p1)
            p2.save()


if __name__ == "__main__":
    populate()
