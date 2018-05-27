from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.apps import apps
from .models import doctors
Patient = apps.get_model('patient', 'Patient')
from django.contrib import messages

import bcrypt
def login(request):
    return render(request, 'doctor/login.html')

def register(request):
    return render(request, 'doctor/register.html')
    
def logsubmit(request):
    errors = doctors.objects.login_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/doctor/login')

    else:
        user1=doctors.objects.get(email=request.POST['email'])
        request.session['doctor_id']=user1.id
        request.session['name']=user1.first_name
        print(request.session['doctor_id'])
        return redirect('/doctor/dashboard')
def regsubmit(request):
    errors = doctors.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/doctor/register')
    # redirect the user back to the form to fix the errors
    else:
        pwd_hash=bcrypt.hashpw(request.POST['pwd'].encode(), bcrypt.gensalt())
        user1=doctors.objects.create(
            first_name=request.POST['first_name'], 
            last_name=request.POST['last_name'], 
            email=request.POST['email'],
            pwd_hash=pwd_hash
        )
        request.session['doctor_id']=user1.id
        request.session['name']=user1.first_name
        return redirect('/doctor/dashboard')
def dashboard(request):
    if 'doctor_id' in request.session:
        doctor=doctors.objects.get(id=request.session['doctor_id'])
        print("-----------------------------------------------------------------")
        patients=Patient.objects.filter(doctor_id=request.session['doctor_id'])
        return render(request, 'doctor/dashboard.html',{'doctor': doctor, 'patients':patients} )
    else:
        messages.error(request, 'you have to log in or register first')
        return redirect('/doctor/login')
def logout(request):
    request.session.clear()
    return redirect('/doctor/login')
def edit(request):
    return render(request, 'doctor/edit.html')
def submit(request):
    if request.method=='POST':
        print('im in the post', request.POST)
        if 'doctor_id' in request.session:

            print(request.POST['email'])
            errors = doctors.objects.edit_validator(request.POST)

            if len(errors)>0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/doctor/edit')
            else:
                user1=doctors.objects.get(id=request.session['id'])
                user1.first_name=request.POST['first_name']
                user1.last_name=request.POST['last_name']
                user1.email=request.POST['email']
                user1.save()
                return redirect('/doctor/dashboard')
        else:
            messages.error(request, 'you have to log in or register first')
        return redirect('/doctor/register')
def patient(request, number):
    patient=patient.objects.get(id=number)
   # if len(entries.objects.filter(patient_id=number))>0
       # entries=entries.objects.get(patient_id=number)
    #else:
     #   entries=""
    return render(request, 'doctor/patient.html', {'patient':patient, })



