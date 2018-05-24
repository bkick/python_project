from django.shortcuts import render, HttpResponse, redirect

def index(request):
    response = "patient INDEX PAGE"
    return HttpResponse(response)