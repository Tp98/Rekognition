from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
def get_image_path(instance, filename):
	return os.path.join('users', str(instance.id), filename)
	
class User(models.Model):
	userId = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
	userImage = models.ImageField(upload_to=get_image_path, blank=True, null=True)
	userFirstname = models.CharField(max_length=100)
	userLastname = models.CharField(max_length=100)
