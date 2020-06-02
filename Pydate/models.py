from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User


####################
# UŻYTKOWNICY
####################
class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birth = models.DateField(null=True)
    sex = models.CharField(max_length=2, null=True)
    personality = models.CharField(max_length=4, null=True)
    description = models.CharField(max_length=300, null=True)
    photo = models.ImageField(null=True, upload_to="images/user_profile_pictures/")
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

    def __str__(self):
        return str(self.questionID)


class PersonalityTestItem(models.Model):
    itemID = models.IntegerField(primary_key=True)
    first_option = models.CharField(max_length=250)
    second_option = models.CharField(max_length=250)

    class Question_Type(models.TextChoices):
        TypeIE = 'IE', _('TypeIE')
        TypeSN = 'SN', _('TypeSN')
        TypeFT = 'FT', _('TypeFT')
        TypeJP = 'JP', _('TypeJP')
    type = models.CharField(
        max_length=2,
        choices=Question_Type.choices,
    )
    inversion = models.BooleanField(default=False)


class PersonalityTestAnswer(models.Model):
    itemID = models.ForeignKey(PersonalityTestItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    answer = models.IntegerField(null=True)


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
    personal_questions_match = models.CharField(max_length=2, choices=Agreement.choices, default=Agreement.AGREE_NONE)
    chatting_match = models.CharField(max_length=2, choices=Agreement.choices, default=Agreement.AGREE_NONE)

    class Meta:
        verbose_name_plural = "Matches"

    def __str__(self):
        return self.user1.username + " + " + self.user2.username


class UserLog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logins = models.IntegerField(default=1)
    likes_sent = models.IntegerField(default=0)
    likes_receive = models.IntegerField(default=0)
    mess_sent = models.IntegerField(default=0)
    mess_receive = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
