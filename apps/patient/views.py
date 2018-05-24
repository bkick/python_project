from django.shortcuts import render, HttpResponse, redirect


# comment
# changed to branch patiens
def index(request):
    response = "patient INDEX PAGE"
    return HttpResponse(response)