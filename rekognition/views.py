from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Employees
from .forms import UploadImage, AddUserForm
import boto3
import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
	return render(request,'home.html')

@login_required
def user(request):
	users = Employees.objects.all()
	return render(request, 'user.html', {'users':users})
	
def model_form_upload(request, pk):
	user = get_object_or_404(Employees, pk=pk)
	if request.method == 'POST':
		form = UploadImage(request.POST, request.FILES)
		if form.is_valid():
			userUpdate = form.save(commit=False)
			userUpdate.image = form.cleaned_data['image']
			userUpdate.save()
			return redirect('userProfile', pk=request.user.pk)
	else:
		form = UploadImage()
	return render(request, 'model_form_upload.html', {'user':user, 'form':form })

@login_required	
def userProfile(request, pk):
	user = Employees.objects.get(pk=pk)
	return render(request, 'userProfile.html', {'user':user})
	
def addUser(request):
	if request.method == 'POST':
		form = AddUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.image = form.cleaned_data['image']
			user.timeOfArrival = datetime.datetime.now()
			user.save()
			return redirect('user')
	else:
		form = AddUserForm()
	return render(request, 'addUser.html', {'form': form})
