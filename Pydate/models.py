from django.db import models

####################
#UŻYTKOWNICY
####################

class user_data(models.Model):
    userID= models.IntegerField(primary_key=True)
    birth = models.DateField(null=False)
    facebook=models.CharField(max_length=100)
    instagram=models.CharField(max_length=100)
    sex=models.CharField(max_length=2,null=False)
    personality=models.IntegerField(null=False)
    description=models.CharField(max_length=300)
    photo=models.FileField()
    location=models.IntegerField()
    nick=models.CharField(max_length=20,null=False)


####################
#PYTANIA UŻYTKOWNIKÓW
####################

class personal_question_content(models.Model):
    questionID= models.IntegerField(primary_key=True)
    content=models.CharField(max_length=250)

class personal_question_user(models.Model):
    questionID=models.ForeignKey(personal_question_content,on_delete=models.CASCADE)
    userID=models.ForeignKey(user_data,on_delete=models.CASCADE)          #ten co pyta

class personal_question_answer(models.Model):
    userID=models.ForeignKey(user_data,on_delete=models.CASCADE)          #ten co odpowiada
    questionID=models.ForeignKey(personal_question_content,on_delete=models.CASCADE)
    content=models.CharField(max_length=300)

####################
#PYTANIA STARTOWE
####################

#TODO: Jarosławie, pisz tu tabele twoją


####################
#CZAT
####################

class chat(models.Model):   #id czatu oraz informacja o tym czy czat nie jest zablokowany
    chatID= models.IntegerField(primary_key=True)
    agreement=models.IntegerField(default=0)

class user_chat(models.Model):  #uzytkownicy podlaczeni do danego czatu
    chatID=models.ForeignKey(chat,on_delete=models.CASCADE)
    userID=models.ForeignKey(user_data,on_delete=models.CASCADE)

class chat_message(models.Model):   #zawartosc czatu
    chatID=models.ForeignKey(chat,on_delete=models.CASCADE)
    message=models.CharField(max_length=300)
    date=models.DateField(auto_now=True)

####################
#STATYSTYKI
####################

class user_log(models.Model):
    userID=models.ForeignKey(user_data,on_delete=models.CASCADE)
    logins=models.IntegerField(default=1)
    likes_sent=models.IntegerField(default=0)
    likes_receive=models.IntegerField(default=0)
    mess_sent=models.IntegerField(default=0)
    mess_receive=models.IntegerField(default=0)