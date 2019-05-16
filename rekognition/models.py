from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
def get_image_path(instance, filename):
	return os.path.join('images/user', str(instance.id), filename)
	
class Employees(models.Model):
	image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
	firstname = models.CharField(max_length=100)
	lastname = models.CharField(max_length=100)
	timeOfArrival = models.DateTimeField(null=True, blank=True)
	timeOfLeaving = models.DateTimeField(null=True, blank=True )
	onBuilding = models.BooleanField(default=False)
		
	def __str__(self):
		return self.firstname
