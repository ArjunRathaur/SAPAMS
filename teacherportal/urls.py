from django.urls import path
from . import views

urlpatterns = [
    path('', views.LandingView.as_view(), name="teacher-landing"),
    path('home/', views.HomeView.as_view(), name="teacher-home"),
    path('account/', views.AccountView.as_view(), name="teacher-account"),
    path('studentgrades/', views.StudentGradesListView.as_view(), name="teacher-grades"),
    path('studentgrades/<str:studentQuery>', views.StudentGradesView.as_view(), name="teacher-viewstudentgrades"),
    path('courses/viewcourse/<str:courseQuery>/', views.ViewCourseView.as_view(), name="teacher-viewcourse"),
    path('courses/new', views.NewCourseView.as_view(), name="teacher-newcourse"),
    path('courses/delete/<str:courseQuery>', views.DeleteCourseView.as_view(), name="teacher-deletecourse"),
    path('assignments/viewassignment/<str:assignmentQuery>', views.ViewAssignmentView.as_view(), name="teacher-viewassignment"),
    path('assignments/viewsubmission/<str:submissionQuery>', views.ViewSubmissionView.as_view(), name="teacher-viewsubmission"),
    path('assignments/new/<str:parentCourse>', views.NewAssignmentView.as_view(), name="teacher-newassignment"),
    path('assignments/delete/<str:assignmentQuery>', views.DeleteAssignmentView.as_view(), name="teacher-deleteassignment"),
    path('disputes/viewdispute/<str:disputeQuery>', views.ViewDisputeView.as_view(), name="teacher-viewdispute"),
    path ('logout/', views.logout, name="teacher-logout")
]
