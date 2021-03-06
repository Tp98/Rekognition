# Generated by Django 2.2 on 2019-05-13 11:33

from django.db import migrations, models
import rekognition.models


class Migration(migrations.Migration):

    dependencies = [
        ('rekognition', '0005_user_onbuilding'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=rekognition.models.get_image_path)),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('timeOfArrival', models.DateTimeField(blank=True, null=True)),
                ('timeOfLeaving', models.DateTimeField(blank=True, null=True)),
                ('onBuilding', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
