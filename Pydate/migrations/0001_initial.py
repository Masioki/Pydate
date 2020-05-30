<<<<<<< HEAD
# Generated by Django 3.0.5 on 2020-04-27 20:34
=======
# Generated by Django 3.0.5 on 2020-05-09 08:57
>>>>>>> origin/master

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
<<<<<<< HEAD
            name='chat',
            fields=[
                ('chatID', models.IntegerField(primary_key=True, serialize=False)),
                ('agreement', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='personal_question_content',
            fields=[
                ('questionID', models.IntegerField(primary_key=True, serialize=False)),
=======
            name='PersonalQuestionContent',
            fields=[
                ('questionID', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
>>>>>>> origin/master
                ('content', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
<<<<<<< HEAD
            name='personality_test_item',
            fields=[
                ('itemID', models.IntegerField(primary_key=True, serialize=False)),
                ('first_option', models.CharField(max_length=250)),
                ('second_option', models.CharField(max_length=250)),
                ('type', models.CharField(choices=[('IE', 'TypeIE'), ('SN', 'TypeSN'), ('FT', 'TypeFT'), ('JP', 'TypeJP')], max_length=2)),
                ('inversion', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='user_data',
            fields=[
                ('userID', models.IntegerField(primary_key=True, serialize=False)),
                ('birth', models.DateField()),
                ('facebook', models.CharField(max_length=100)),
                ('instagram', models.CharField(max_length=100)),
                ('sex', models.CharField(max_length=2)),
                ('personality', models.CharField(max_length=4)),
                ('description', models.CharField(max_length=300)),
                ('photo', models.FileField(upload_to='')),
                ('location', models.IntegerField()),
                ('nick', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='user_log',
=======
            name='UserLog',
>>>>>>> origin/master
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logins', models.IntegerField(default=1)),
                ('likes_sent', models.IntegerField(default=0)),
                ('likes_receive', models.IntegerField(default=0)),
                ('mess_sent', models.IntegerField(default=0)),
                ('mess_receive', models.IntegerField(default=0)),
<<<<<<< HEAD
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pydate.user_data')),
            ],
        ),
        migrations.CreateModel(
            name='user_chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chatID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pydate.chat')),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pydate.user_data')),
            ],
        ),
        migrations.CreateModel(
            name='personality_test_answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.IntegerField(null=True)),
                ('itemID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pydate.personality_test_item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='personal_question_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questionID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pydate.personal_question_content')),
            ],
        ),
        migrations.CreateModel(
            name='personal_question_answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=300)),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pydate.user_data')),
            ],
        ),
        migrations.CreateModel(
            name='chat_message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=300)),
                ('date', models.DateField(auto_now=True)),
                ('chatID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pydate.chat')),
=======
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('birth', models.DateField()),
                ('facebook', models.CharField(max_length=100)),
                ('instagram', models.CharField(max_length=100)),
                ('sex', models.CharField(max_length=2)),
                ('personality', models.IntegerField()),
                ('description', models.CharField(max_length=300)),
                ('photo', models.ImageField(upload_to='')),
                ('location', models.IntegerField()),
                ('nick', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalQuestionUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questionID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pydate.PersonalQuestionContent')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalQuestionAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=300)),
                ('questionID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pydate.PersonalQuestionContent')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
>>>>>>> origin/master
            ],
        ),
    ]
