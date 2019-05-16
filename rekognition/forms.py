from django import forms
from .models import Employees

class UploadImage(forms.ModelForm):
	class Meta:
		model = Employees
		fields = ['image',]

class AddUserForm(forms.ModelForm):
	class Meta : 
		model = Employees
		fields = ['firstname', 'lastname', 'image',]
