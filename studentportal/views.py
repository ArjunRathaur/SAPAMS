from django.shortcuts import render
from django.http import HttpResponse
from .utils import dbutils, miscutils
# Create your views here.

currentUserID = "a267664a8b2e11ea9e62001b21254ea4" # (studentuser0), cookies/auth are not yet implemented so this is temporarily hard coded to showcase sorting/searching

def landing(request):
    return render(request, 'studentportal/landing.html')

def home(request):
    return render(request, 'studentportal/home.html')

def grades(request):

    # Set up context for displaying request response
    context = { 
        "assignmentSubmissions": list(), 
        "assignmentSubmissionsSorted": list()
    }

    # SORTING AND SEARCHING
    # we get the student, then we go through all their courses and grab their assignments, find their submission, and add all their submissions to an array.
    student = dbutils.loadStudent(currentUserID)
    for course in dbutils.resolveIDList(student.courseIDs, 'Course'):
        for assignment in dbutils.resolveIDList(course.assignmentIDs, 'Assignment'):
            for assignmentSubmission in dbutils.resolveIDList(assignment.submissionIDs, 'AssignmentSubmission'):
                if assignmentSubmission.submitterID == currentUserID:
                    context["assignmentSubmissions"].append(assignmentSubmission)

    # context["assignmentSubmissionsSorted"] = miscutils.selectionSortGrades(context["assignmentSubmissions"].copy()) # SELECTION SORT
    # context["assignmentSubmissionsSorted"] = miscutils.bubbleSortGrades(context["assignmentSubmissions"].copy()) # BUBBLE SORT
    
    # built in sort functionality usage
    context["assignmentSubmissionsSorted"] = sorted(context["assignmentSubmissions"].copy(), key = lambda x: x.grade, reverse=False)

    return render(request, 'studentportal/grades.html', context)

def courses(request):
    return render(request, 'studentportal/courses.html')












