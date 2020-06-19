from django.urls import path
from . import views

urlpatterns = [
    path('', views.LandingView.as_view(), name="student-landing"),
    path('home/', views.HomeView.as_view(), name="student-home"),
    path('account/', views.AccountView.as_view(), name="student-account"),
    path('grades/', views.GradesView.as_view(), name="student-grades"),
    path('courses/viewcourse/<str:courseQuery>/', views.ViewCourseView.as_view(), name="student-viewcourse"),
    path('assignments/viewassignment/<str:assignmentQuery>', views.ViewAssignmentView.as_view(), name="student-viewassignment"),
    path('disputes/viewdispute/<str:disputeQuery>', views.ViewDisputeView.as_view(), name="student-viewdispute"),
    path ('disputes/new/<str:parentAssignment>', views.NewDisputeView.as_view(), name="student-newdispute"),
    path ('logout/', views.logout, name="student-logout")
]
