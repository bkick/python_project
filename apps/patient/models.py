from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from bcrypt import checkpw
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class PatientManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        # FIRST NAME
        if len(postData['first_name']) < 1:
            errors['first_name'] = 'FIRST name cannot be empty'
        elif len(postData['first_name']) < 3:
            errors['first_name'] = 'FIRST name must be 3+ chars'
        # LAST NAME
        if len(postData['last_name']) < 1:
            errors['last_name'] = 'LAST name cannot be empty'
        elif len(postData['last_name']) < 3:
            errors['last_name'] = 'LAST name must be 3+'
        # EMAIL
        if len(postData['email']) < 1:
            errors['email'] = 'EMAIL cannot be empty'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'EMAIL NOT valid'
        # if email exists in DB 
        if Patient.objects.filter(email=postData['email']):
            errors['email'] = 'EMAIL already exists!!!'
        # PASSWORD
        if len(postData['password']) < 1:
            errors['password'] = 'Password cannot be BLANK!'
        elif len(postData['password']) <3:
            errors['password'] = 'Password has to be AT LEAST 3 characters!'
        if postData['password'] != postData['password_confirm']:
            errors['password'] = 'Pws do not match!'
        return errors

    def login_validator(self, postData):
        errors = {}
        # check if email is valid
        if len(postData['email']) < 1:
            errors['email'] = 'EMAIL cannot be empty'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'EMAIL NOT valid'
        # check if email exists in DB
        if len(Patient.objects.filter(email=postData['email'])) < 1:
            print("EMAIL exits in db continue to pw validation !!!")
        else: # if email exists contiue to password check
            patient_check = Patient.objects.filter(email=postData['email'])
            if len(postData['password']) < 1:
                errors['password'] = 'password cannot be empty'
            elif not checkpw(postData['password'].encode(), patient_check[0].password.encode()):
                errors['password'] = 'pass doesnt match'
        return errors

    # def update_validator(self, postData):
    #     errors = {}
    #     # FIRST NAME
    #     if len(postData['first_name']) < 1:
    #         errors['first_name'] = 'FIRST name cannot be empty'
    #     elif len(postData['first_name']) < 3:
    #         errors['first_name'] = 'FIRST name must be 3+ chars'
    #     # LAST NAME
    #     if len(postData['last_name']) < 1:
    #         errors['last_name'] = 'LAST name cannot be empty'
    #     elif len(postData['last_name']) < 1:
    #         errors['last_name'] = 'LAST name cannot be empty'
    #     # EMAIL
    #     if len(postData['email']) < 1:
    #         errors['email'] = 'EMAIL cannot be empty'
    #     elif not EMAIL_REGEX.match(postData['email']):
    #         errors['email'] = 'EMAIL NOT valid'
    #     # if email exists in DB 
    #     if User.objects.filter(email=postData['email']):
    #         errors['email'] = 'EMAIL already exists!!!'
    #     return errors


class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    dob = models.DateField()
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    weight = models.SmallIntegerField()
    height = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    doctor_id=models.IntegerField(default=1)
    objects = PatientManager()

