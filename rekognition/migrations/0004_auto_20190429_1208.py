# Generated by Django 2.2 on 2019-04-29 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rekognition', '0003_user_userimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='userFirstname',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='userImage',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='userLastname',
            new_name='lastname',
        ),
        migrations.AddField(
            model_name='user',
            name='timeOfArrival',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='timeOfLeaving',
            field=models.DateTimeField(null=True),
        ),
    ]
