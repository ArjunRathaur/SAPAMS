from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name="student-landing"),
    path('home/', views.home, name="student-home"),
    path('grades/', views.grades, name="student-grades"),
    path('courses/', views.courses, name="student-courses")
]
