from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def landing(request):
    return render(request, 'teacherportal/landing.html ')

def home(request):
    return render(request, 'teacherportal/home.html ')

def grades(request):
    return render(request, 'teacherportal/grades.html ')

def courses(request):
    return render(request, 'teacherportal/courses.html ')