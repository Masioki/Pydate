from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class Person2(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)