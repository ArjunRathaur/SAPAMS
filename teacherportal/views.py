from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def landing(request):
    return HttpResponse("<h1>The teacher landing page will go here</h1>")

def home(request):
    return HttpResponse("<h1>The teacher home page will go here</h1>")

def grades(request):
    return HttpResponse("<h1>The teacher grades page will go here</h1>")

def courses(request):
    return HttpResponse("<h1>The teacher courses page will go here</h1>")