# Generated by Django 3.0.5 on 2020-05-09 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pydate', '0006_auto_20200509_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='description',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='instagram',
            field=models.CharField(max_length=100, null=True),
        ),
    ]