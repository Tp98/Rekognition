# Generated by Django 2.2 on 2019-04-29 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rekognition', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='userId',
        ),
        migrations.RemoveField(
            model_name='user',
            name='userImage',
        ),
    ]
