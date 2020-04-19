from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def landing(request):
    return HttpResponse('<h1>Teacher/Student portal selection will go here</h1>')