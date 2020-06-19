from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from django.views.generic import TemplateView

from studentportal.forms import LoginForm, SubmitAssignmentForm, ChangePasswordForm, CreateDisputeForm, DisputeResponseForm

import hashlib
import datetime
import random

from .utils import dbutils, miscutils
from .utils.assignmentsubmission import AssignmentSubmission
from .utils.dispute import Dispute
from .utils.disputeresponse import DisputeResponse
from .utils.teacher import Teacher

# Create your views here.

class LandingView(TemplateView):
    template_name = 'studentportal/landing.html'

    def get(self, request):
        # if already authenticated, redirect to student home
        if request.COOKIES.get('authed_user'):
            return redirect('student-home')
        # else, prompt login
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            pw = form.cleaned_data['password']
            
            # Check email validity
            student = dbutils.loadStudentByEmail(email)
            if student == False:
                return render(request, self.template_name, {'form': LoginForm(), 'error': 'Invalid Credentials.'})
            elif hashlib.sha256(pw.encode()).hexdigest() != student.password:
                # check if pass incorrect
                return render(request, self.template_name, {'form': LoginForm(), 'error': 'Invalid Credentials.'})
            else:
                # correct; authenticate with cookie of ID
                response = redirect('student-home')
                response.set_cookie("authed_user", student.ID)
                return response


def logout(request):
    # redirect to landing and remove cookie
    response = redirect('main-landing')
    if (request.COOKIES.get('authed_user') != None):
        response.delete_cookie("authed_user")
    return response

class HomeView(TemplateView):
    template_name = 'studentportal/home.html'

    def get(self, request):
        # if not auth'd, redirect
        if not request.COOKIES.get('authed_user'):
            return redirect('student-landing')
        # return webpage rendered with user's course objects
        
        return render(request, self.template_name, {'courses': dbutils.resolveIDList(dbutils.loadStudent(request.COOKIES.get('authed_user')).courseIDs, 'Course')})

class GradesView(TemplateView):
    template_name = 'studentportal/grades.html'

    def get(self, request):
        # if not authenticated, redirect to student home
        if not request.COOKIES.get('authed_user'):
            return redirect('student-landing')

        # Set up context for displaying request response
        student = dbutils.loadStudent(request.COOKIES.get('authed_user'))
        context = { 
            "assignmentSubmissions": list(), 
            "assignmentSubmissionsSorted": list(),
            "average": student.calculateAverage()
        }

        # SORTING AND SEARCHING
        # we get the student, then we go through all their courses and grab their assignments, find their submission, and add all their submissions to an array.
        for course in dbutils.resolveIDList(student.courseIDs, 'Course'):
            for assignment in dbutils.resolveIDList(course.assignmentIDs, 'Assignment'):
                for assignmentSubmission in dbutils.resolveIDList(assignment.submissionIDs, 'AssignmentSubmission'):
                    if assignmentSubmission.submitterID == request.COOKIES.get('authed_user') and assignmentSubmission.grade != -1:
                        context["assignmentSubmissions"].append([assignment, assignmentSubmission])

        # context["assignmentSubmissionsSorted"] = miscutils.selectionSortGrades(context["assignmentSubmissions"].copy()) # SELECTION SORT
        # context["assignmentSubmissionsSorted"] = miscutils.bubbleSortGrades(context["assignmentSubmissions"].copy()) # BUBBLE SORT
        
        # built in sort functionality usage
        context["assignmentSubmissionsSorted"] = sorted(context["assignmentSubmissions"].copy(), key = lambda x: x[1].grade, reverse=True)

        return render(request, self.template_name, context)

class ViewCourseView(TemplateView):
    template_name = 'studentportal/viewcourse.html'

    def get(self, request, courseQuery):
        
        if not request.COOKIES.get('authed_user'):
            # Not logged in
            return redirect('student-landing')

        course = dbutils.loadCourse(courseQuery)
        if course == False:
            # Course doesn't exist
            return render(request, self.template_name, {'error': 'Course could not be found.'})
        if request.COOKIES.get('authed_user') not in course.studentIDs:
            # Student not in course, and therefore cannot view the course
            return render(request, self.template_name, {'error': 'You do not have permission to view this course.'})
        return render(request, self.template_name, {'course': course, 'assignments': dbutils.resolveIDList(course.assignmentIDs, 'Assignment')})


    def post(self, request):
        pass

class ViewAssignmentView(TemplateView):
    template_name = 'studentportal/viewassignment.html'

    def get(self, request, assignmentQuery):
        
        if not request.COOKIES.get('authed_user'):
            # Not logged in
            return redirect('student-landing')

        assignment = dbutils.loadAssignment(assignmentQuery)
        if assignment == False:
            # Assignment doesn't exist
            return render(request, self.template_name, {'error': 'Assignment could not be found.'})
        if request.COOKIES.get('authed_user') not in dbutils.loadCourse(assignment.courseID).studentIDs:
            # Student not in assignment's course, and therefore cannot view the assignment
            return render(request, self.template_name, {'error': 'You do not have permission to view this Assignment.'})
        userSubmission = None
        userGrade = None
        # loop and find submission
        for submission in dbutils.resolveIDList(assignment.submissionIDs, 'AssignmentSubmission'):
            if submission.submitterID == request.COOKIES.get('authed_user'):
                userSubmission = submission
                userGrade = submission.grade
                break
        
        disputes = []
        # iterate and make list of disputes under the assignment
        for dispute in dbutils.resolveIDList(assignment.disputeIDs, 'Dispute'):
            if dispute.creatorID == request.COOKIES.get('authed_user'):

                lastResponse = dbutils.loadDisputeResponse(dispute.responseIDs[-1])
                previewContent = lastResponse.content

                user = dbutils.loadStudent(lastResponse.authorID)
                displayName = ""
                if user == False:
                    user = dbutils.loadTeacher(lastResponse.authorID)
                    displayName = user.prefix + " " + user.lastName
                else:
                    displayName = user.firstName + " " + user.lastName

                # Formatting for webpage rendering
                # Cut off at length 50 to ensure text fits on webpage
                if len(previewContent) > 50:
                    dispute.preview = displayName + " said: \"" + previewContent[0:50] + "...\""
                else:
                    dispute.preview = displayName + " said: \"" + previewContent + "\""
                disputes.append(dispute)

        form = SubmitAssignmentForm()

        # formatting so -1 doesn't appear
        if userGrade == -1:
            userGrade = "None"

        return render(request, self.template_name, {'assignment': assignment, 'grade': userGrade, 'submission': userSubmission, 'form': form, 'assignmentID': assignmentQuery, 'disputes': disputes})


    def post(self, request, assignmentQuery):
        form = SubmitAssignmentForm(request.POST)
        if form.is_valid():

            # submit and add submission to assignment IDs array
            submissionText = form.cleaned_data['text']
            submission = AssignmentSubmission(request.COOKIES.get('authed_user'), datetime.datetime.now(), [submissionText])
            dbutils.saveAssignmentSubmission(submission)
            assignment = dbutils.loadAssignment(assignmentQuery)
            assignment.addSubmission(submission)
            dbutils.saveAssignment(assignment)

            userGrade = None

            return render(request, self.template_name, {'assignment': assignment, 'grade': userGrade, 'submission': submission, 'assignmentID': assignmentQuery})

class AccountView(TemplateView):
    template_name = 'studentportal/account.html'

    def get(self, request):

        if not request.COOKIES.get('authed_user'):
            # Not logged in
            return redirect('student-landing')

        form = ChangePasswordForm()

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            student = dbutils.loadStudent(request.COOKIES.get('authed_user'))
            current = form.cleaned_data['current']
            new1 = form.cleaned_data['new1']
            new2 = form.cleaned_data['new2']

            if hashlib.sha256(current.encode()).hexdigest() != student.password:
                # check if current password correct; this activates if no
                form = ChangePasswordForm()
                return render(request, self.template_name, {'form': form, 'error': "Password incorrect."})
            elif new1 != new2:
                # two new password entries don't match
                form = ChangePasswordForm()
                return render(request, self.template_name, {'form': form, 'error': 'Passwords did not match.'})
            else:
                # update password and logout
                student.password = hashlib.sha256(new1.encode()).hexdigest()
                dbutils.saveStudent(student)
                return redirect('student-logout')

class NewDisputeView(TemplateView):
    template_name = 'studentportal/newdispute.html'

    def get(self, request, parentAssignment):
        
        if not request.COOKIES.get('authed_user'):
            # Not logged in
            return redirect('student-landing')

        assignment = dbutils.loadAssignment(parentAssignment)
        if assignment == False:
            # Assignment doesn't exist
            return render(request, self.template_name, {'error': 'The parent assignment could not be found.'})
        if request.COOKIES.get('authed_user') not in dbutils.loadCourse(assignment.courseID).studentIDs:
            # Student not in assignment's course, and therefore cannot create a dispute here.
            return render(request, self.template_name, {'error': 'You do not have permission to create a dispute under this assignment.'})

        form = CreateDisputeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, parentAssignment):
        form = CreateDisputeForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['text']
            
            # create dispute and add the response to it, then make necessary ID associations in the database.
            firstResponse = DisputeResponse(request.COOKIES.get('authed_user'), message)
            dbutils.saveDisputeResponse(firstResponse)

            assignment = dbutils.loadAssignment(parentAssignment)
            course = dbutils.loadCourse(assignment.courseID)
            teachers = dbutils.resolveIDList(course.teacherIDs, 'Teacher')
            teacher = random.choice(teachers)
            
            dispute = Dispute(request.COOKIES.get('authed_user'), teacher.ID, [firstResponse.ID])
            dbutils.saveDispute(dispute)

            assignment.addDispute(dispute)
            dbutils.saveAssignment(assignment)

            return redirect('student-viewassignment', assignmentQuery=parentAssignment)


class ViewDisputeView(TemplateView):
    template_name = 'studentportal/viewdispute.html'

    def get(self, request, disputeQuery):

        if not request.COOKIES.get('authed_user'):
            # Not logged in
            return redirect('student-landing')

        dispute = dbutils.loadDispute(disputeQuery)
        if dispute == False:
            # Dispute doesn't exist
            return render(request, self.template_name, {'error': 'Dispute could not be found.'})
        if request.COOKIES.get('authed_user') not in [dispute.creatorID, dispute.handlerID]:
            # Student not member of dispute, and therefore cannot view it
            return render(request, self.template_name, {'error': 'You do not have permission to view this Dispute.'})

        form = DisputeResponseForm()

        responses = []

        # iterate disputeresponses to get formatted array of disputeresponses to display.
        for disputeResponse in dbutils.resolveIDList(dbutils.loadDispute(disputeQuery).responseIDs, 'DisputeResponse'):
            user = dbutils.loadStudent(disputeResponse.authorID)
            displayName = ""
            if user == False:
                user = dbutils.loadTeacher(disputeResponse.authorID)
                displayName = user.prefix + " " + user.lastName
            else:
                displayName = user.firstName + " " + user.lastName

            responses.append({
                'displayName': displayName,
                'content': disputeResponse.content
            })

        return render(request, self.template_name, {'form': form, 'responses': responses, 'dispute': dispute})

    def post(self, request, disputeQuery):
        form = DisputeResponseForm(request.POST)

        if form.is_valid():
            message = form.cleaned_data['text']
            # create response and save it
            newResponse = DisputeResponse(request.COOKIES.get('authed_user'), message)
            dbutils.saveDisputeResponse(newResponse)

            # add response to parent dispute class and save
            dispute = dbutils.loadDispute(disputeQuery)
            dispute.addResponse(newResponse)
            dbutils.saveDispute(dispute)

            form = DisputeResponseForm()

            responses = []

            # render page (similar to  get)
            for disputeResponse in dbutils.resolveIDList(dbutils.loadDispute(disputeQuery).responseIDs, 'DisputeResponse'):
                user = dbutils.loadStudent(disputeResponse.authorID)
                displayName = ""
                if user == False:
                    user = dbutils.loadTeacher(disputeResponse.authorID)
                    displayName = user.prefix + " " + user.lastName
                else:
                    displayName = user.firstName + " " + user.lastName

                responses.append({
                    'displayName': displayName,
                    'content': disputeResponse.content
                })

            return render(request, self.template_name, {'form': form, 'responses': responses, 'dispute': dispute})

