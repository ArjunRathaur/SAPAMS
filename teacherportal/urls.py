from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name="teacher-landing"),
    path('home/', views.home, name="teacher-home"),
    path('grades/', views.grades, name="teacher-grades"),
    path('courses/', views.courses, name="teacher-courses")
]
