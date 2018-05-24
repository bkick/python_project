from django.shortcuts import render, HttpResponse, redirect


# comment
def index(request):
    response = "patient INDEX PAGE"
    return HttpResponse(response)