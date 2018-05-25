from __future__ import unicode_literals
from django.db import models
from patient.models import *
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def edit_validator(self, postData):
        errors={}
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_val'] = "You must enter a valid email"
        if len(postData['email']) < 1:
            errors["email"] = "E-mail can not be empty"
        if len(postData['first_name']) < 1:
            errors["first_name"] = "Please enter your first name"
        if len(postData['last_name']) < 1:
            errors["last_name"] = "Please enter your last name"
        return errors
    def basic_validator(self, postData):
        errors = {}
        if len(doctors.objects.filter(email=postData['email']))>0:
            errors['email_exist'] = "That email has already been registered with us"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_val'] = "You must enter a valid email"
        if len(postData['email']) < 1:
            errors["email"] = "E-mail can not be empty"
        if len(postData['first_name']) < 1:
            errors["first_name"] = "Please enter your first name"
        if len(postData['last_name']) < 1:
            errors["last_name"] = "Please enter your last name"
        if len(postData['pwd'])<1:
            errors['pwd']="Password cannot be empty"
        if postData['pwd']!= postData['pwd_conf']:
            errors['pwd_conf']="Password and confirm password do not match"
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(doctors.objects.filter(email=postData['email']))>0:
            user=doctors.objects.get(email=postData['email'])
            if bcrypt.checkpw(postData['pwd'].encode(), user.pwd_hash.encode()):
                return errors
            else:
                errors['password']='your password is incorrect'
        else:
            errors['email']='that email is not registered with us'

        return errors 
class doctors(models.Model):
    email=models.CharField(max_length=100)
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    pwd_hash=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = UserManager()

