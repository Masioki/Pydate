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
    photo = models.ImageField(null=True, upload_to="images/user_profile_pictures/")
    latitude = models.DecimalField(max_digits=9, decimal_places=5, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=5, null=True)
    searching_for = models.CharField(max_length=5, null=True)

    def __str__(self):
        return self.user.username


####################
# PYTANIA UŻYTKOWNIKÓW
####################


class PersonalQuestionContent(models.Model):
    questionID = models.AutoField(auto_created=True, serialize=False, primary_key=True)
    content = models.CharField(max_length=250)

    def __str__(self):
        return str(self.questionID)


class PersonalQuestionUser(models.Model):
    questionID = models.ForeignKey(PersonalQuestionContent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # ten co pyta

    def __str__(self):
        return str(self.questionID)


class PersonalQuestionAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # ten co odpowiada
    questionID = models.ForeignKey(PersonalQuestionContent, on_delete=models.CASCADE)
    content = models.CharField(max_length=300, blank=False, null=False)

    def __str__(self):
        return str(self.questionID)


####################
# PYTANIA STARTOWE
####################

# TODO

####################
# STATYSTYKI
####################


class Match(models.Model):
    class Agreement(models.TextChoices):
        AGREE_NONE = '00'
        AGREE_1_TO_2 = '01'
        AGREE_2_TO_1 = '10'
        AGREE_BOTH = '11'
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="user2")
    #Jak w answers dam serce to zmieniam wartosc personal_questions_match
    personal_questions_match = models.CharField(max_length=2, choices=Agreement.choices, default=Agreement.AGREE_NONE)
    #Jak na glownej dam serce to zmieniam wartosc chatting_match
    chatting_match = models.CharField(max_length=2, choices=Agreement.choices, default=Agreement.AGREE_NONE)
    #Jak chatting_match jest rowny AGREE_NONE to te osoby nie maja prawa juz NIGDY siebie spotkac

    class Meta:
        verbose_name_plural = "Matches"

    def __str__(self):
        return self.user1.username + " + " + self.user2.username


class UserLog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='logs')
    logins = models.IntegerField(default=1)
    likes_sent = models.IntegerField(default=0)
    likes_receive = models.IntegerField(default=0)
    mess_sent = models.IntegerField(default=0)
    mess_receive = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
