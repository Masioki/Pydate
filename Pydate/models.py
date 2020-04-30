from django.db import models
from django.contrib.auth.models import User


####################
# UŻYTKOWNICY
####################

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth = models.DateField(null=False)
    facebook = models.CharField(max_length=100)
    instagram = models.CharField(max_length=100)
    sex = models.CharField(max_length=2, null=False)
    personality = models.IntegerField(null=False)
    description = models.CharField(max_length=300)
    photo = models.ImageField()
    location = models.IntegerField()
    nick = models.CharField(max_length=20, null=False)


####################
# PYTANIA UŻYTKOWNIKÓW
####################


class PersonalQuestionContent(models.Model):
    questionID = models.AutoField(auto_created=True, serialize=False, primary_key=True)
    content = models.CharField(max_length=250)


class PersonalQuestionUser(models.Model):
    questionID = models.ForeignKey(PersonalQuestionContent, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # ten co pyta


class PersonalQuestionAnswer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # ten co odpowiada
    questionID = models.ForeignKey(PersonalQuestionContent, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)


####################
# PYTANIA STARTOWE
####################

# TODO

####################
# STATYSTYKI
####################


class UserLog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logins = models.IntegerField(default=1)
    likes_sent = models.IntegerField(default=0)
    likes_receive = models.IntegerField(default=0)
    mess_sent = models.IntegerField(default=0)
    mess_receive = models.IntegerField(default=0)
