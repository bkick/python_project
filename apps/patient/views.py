from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.apps import apps
from django.contrib import messages
import bcrypt
doctors = apps.get_model('doctor', 'doctors')

# landing page
def home(request):
    print('\n   --> home.html <--')
    return render(request, 'patient/home.html')

def patient_landing(request):
    print('\n   --> patient_landing.html <--')
    return render(request, 'patient/patient_landing.html')

def index_html(request):
    print('\n   --> index html page <--')
    return render(request, 'patient/index.html')

def login_html(request):
    print('\n   --> login html <--')
    return render(request, 'patient/patient_login.html')

def register_html(request):
    doctor = doctors.objects.all()
    context = {
    'doctor':doctor
    }
    print('\n   --> register html <--')
    return render(request, 'patient/patient_register.html', context)

def registration_method(request):
    print('\n   --> registration method <--')
    if request.method == 'POST':
        errors = Patient.objects.registration_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/patient/register_html')
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            Patient.objects.create(first_name=request.POST['first_name'], 
                                last_name=request.POST['last_name'], 
                                email=request.POST['email'], 
                                dob=request.POST['bday'], 
                                password=hashed_pw,
                                weight=request.POST['weight'],
                                height=request.POST['height'],
                                doctor_id=request.POST['doctor'])
            request.session['patient_id'] = Patient.objects.get(email=request.POST['email']).id
            request.session['patient_first_name'] = Patient.objects.get(email=request.POST['email']).first_name
            request.session['patient_last_name'] = Patient.objects.get(email=request.POST['email']).last_name
            return redirect('/patient/dashboard_html')

def login_method(request):
    if request.method == 'POST':
        errors = Patient.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/patient/login_html')
        else:
            request.session['patient_id'] = Patient.objects.get(email=request.POST['email']).id
            return redirect('/patient/dashboard_html')

def dashboard_html(request):
    print('\n   --> dashboard <--')
    if 'patient_id' not in request.session:
        return redirect("/patient")
    else:
        patient = Patient.objects.get(id=request.session['patient_id'])
        doctor = doctors.objects.get(id=patient.doctor_id)
        return render(request, 'patient/patient_dashboard.html', {'doctor': doctor, 'patient':patient})

def update_health(request):
    print('\n   --> update_health method <--')
    # update db with current weight and height
    return redirect('/patient/dashboard_html')

def that_info_html(request):
    print('\n   --> info <--')
    return render(request, 'patient/that_info.html')

def edit_profile_html(request):
    print('\n   --> info <--')
    patient = Patient.objects.get(id=request.session['patient_id'])
    return render(request, 'patient/edit_profile.html', {'patient': patient})

def moreDetails(request):
    print('\n   --> moreDetails html <--')
    return render(request, 'patient/moreDetails.html')

def moreDetails_method(request):
    print('\n   --> moreDetails method <--')
    if request.method == 'POST':
            errors = Patient.objects.moreDetails_validator(request.POST)
            if len(errors):
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/patient/moreDetails')
            else:
                p = Patient.objects.get(id=request.session['patient_id'])
                p.address = request.POST['address']
                p.address2 = request.POST['address2']
                p.city = request.POST['city']
                p.state = request.POST['state']
                p.zipcode = request.POST['zip']
                p.weight = request.POST['weight']
                p.height = request.POST['height']
                p.save()
                return redirect('/patient/dashboard_html')


def logout(request):
    print("\n======> Server > Logout")
    request.session.clear()
    return redirect('/patient')

def about(request):
    print('\n ======> seerver > about')
    return render(request, 'patient/about.html')