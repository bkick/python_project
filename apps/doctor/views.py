from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
def index(request):
	return render(request,'index.html')
    
def login(request):
    errors = users.objects.login_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    else:
        user1=users.objects.get(email=request.POST['email'])
        request.session['id']=user1.id
        request.session['name']=user1.first_name
        return redirect('/success')
def register(request):
    errors = users.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    # redirect the user back to the form to fix the errors
    else:
        pwd_hash=bcrypt.hashpw(request.POST['pwd'].encode(), bcrypt.gensalt())
        user1=users.objects.create(
            first_name=request.POST['first_name'], 
            last_name=request.POST['last_name'], 
            email=request.POST['email'],
            pwd_hash=pwd_hash
        )
        request.session['id']=user1.id
        request.session['name']=user1.first_name
        return redirect('/success')
def success(request):
    if 'id' in request.session:
        return render(request, 'success.html')
    else:
        messages.error(request, 'you have to log in or register first')
        return redirect('/')
def logout(request):
    request.session.clear()
    return redirect('/')
