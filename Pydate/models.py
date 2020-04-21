from django.db import models

class user_static_data(models.Model):
    userID= models.IntegerField(primary_key=True)
    birth = models.DateField(null=False)
    facbook=models.CharField(max_length=100)
    instagram=models.CharField(max_length=100)
    sex=models.IntegerField(null=False)
    personality=models.IntegerField(null=False)

class user_dynamic_data(models.Model):
    userID = models.ForeignKey(user_static_data)
    descrition=models.CharField(max_length=300)
    photo=models.FileField()
    location=models.IntegerField()
    nick=models.CharField(max_length=20,null=False)

class personal_question_content(models.Model):
    questionID= models.IntegerField(primary_key=True)
    userID=models.ForeignKey(user_static_data)
    content=models.CharField(max_length=250)

class personal_question_users(models.Model):
    questionID=models.ForeignKey(personal_question_content)
    userID=models.ForeignKey(user_static_data)

class personal_question_answear(models.Model):
    userID=models.ForeignKey(user_static_data)
    questionID=models.ForeignKey(personal_question_content)
    content=models.CharField(max_length=300)

class starter_quetion(models.Model):
    questionID= models.IntegerField(primary_key=True)
    content=models.CharField(max_length=250)

class chat(models.Model):
    chatID= models.IntegerField(primary_key=True)
    user1ID=models.ForeignKey(user_static_data)
    user2ID=models.ForeignKey(user_static_data)
    agreement=models.IntegerField(default=0)

class chat_message(models.Model):
    chatID=models.ForeignKey(chat)
    message=models.CharField(max_length=300)
    date=models.DateField(auto_now=True())

class user_log(models.Model):
    userID=models.ForeignKey(user_static_data)
    logins=models.IntegerField(default=1)
    likes_sent=models.IntegerField(default=0)
    likes_receive=models.IntegerField(default=0)
    mess_sent=models.IntegerField(default=0)
    mess_receive=models.IntegerField(default=0)
