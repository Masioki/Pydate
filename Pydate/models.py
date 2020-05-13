from django.db import models
from django.contrib.auth.models import User


####################
# UŻYTKOWNICY
####################

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birth = models.DateField(null=True)
    sex = models.CharField(max_length=2, null=True)
    personality = models.IntegerField(null=True)
    description = models.CharField(max_length=300, null=True)
    photo = models.ImageField(null=True)
    location = models.IntegerField(null=True)
    searching_for = models.CharField(max_length=5, null=True)

    def __str__(self):
        return self.user.username


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
