from django.db import models

class user_static_data(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)