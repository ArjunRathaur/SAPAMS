from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from django.views.generic import TemplateView

from teacherportal.forms import LoginForm, ChangePasswordForm, CreateDisputeForm, DisputeResponseForm, ConfirmForm, GradeForm, CreateCourseForm, CreateAssignmentForm

import hashlib
import datetime
import random

from .utils import dbutils, miscutils
from .utils.assignmentsubmission import AssignmentSubmission
from .utils.dispute import Dispute
from .utils.disputeresponse import DisputeResponse
from .utils.teacher import Teacher
from .utils.course import Course
from .utils.assignment import Assignment

# Create your views here.

class LandingView(TemplateView):

    template_name = 'teacherportal/landing.html'

    def get(self, request):
        # if already authenticated, redirect to teacher home
        if request.COOKIES.get('authed_teacher'):
            return redirect('teacher-home')
        # else, prompt login
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            pw = form.cleaned_data['password']
            
            # Check email validity
            teacher = dbutils.loadTeacherByEmail(email)
            if teacher == False:
                # email bad
                return render(request, self.template_name, {'form': LoginForm(), 'error': 'Invalid Credentials.'})
            elif hashlib.sha256(pw.encode()).hexdigest() != teacher.password:
                # password bad
                return render(request, self.template_name, {'form': LoginForm(), 'error': 'Invalid Credentials.'})
            else:
                # valid; authenticate cookie
                response = redirect('teacher-home')
                response.set_cookie("authed_teacher", teacher.ID)
                return response


def logout(request):
    # redirect them to logout and delete cookie
    response = redirect('main-landing')
    if (request.COOKIES.get('authed_teacher') != None):
        response.delete_cookie("authed_teacher")
    return response

class HomeView(TemplateView):
    template_name = 'teacherportal/home.html'

    def get(self, request):
        # if already authenticated, redirect to teacher home
        if not request.COOKIES.get('authed_teacher'):
            return redirect('teacher-landing')
        # else, prompt login

        # just render the webpage with a list of their courses
        return render(request, self.template_name, {'courses': dbutils.resolveIDList(dbutils.loadTeacher(request.COOKIES.get('authed_teacher')).courseIDs, 'Course')})

class StudentGradesView(TemplateView):
    template_name = 'teacherportal/studentgrades.html'

    def get(self, request, studentQuery):
        # if not authenticated, redirect to teacher home
        if not request.COOKIES.get('authed_teacher'):
            return redirect('teacher-landing')

        # Set up context for displaying request response
        student = dbutils.loadStudent(studentQuery)
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
                    if assignmentSubmission.submitterID == student.ID and assignmentSubmission.grade != -1:
                        context["assignmentSubmissions"].append([assignment, assignmentSubmission])

        # context["assignmentSubmissionsSorted"] = miscutils.selectionSortGrades(context["assignmentSubmissions"].copy()) # SELECTION SORT
        # context["assignmentSubmissionsSorted"] = miscutils.bubbleSortGrades(context["assignmentSubmissions"].copy()) # BUBBLE SORT
        
        # built in sort functionality usage
        context["assignmentSubmissionsSorted"] = sorted(context["assignmentSubmissions"].copy(), key = lambda x: x[1].grade, reverse=True)

        context['studentName'] = student.firstName + " " + student.lastName

        # render using sorted grades, ordered highest grade to lowest grade.
        return render(request, self.template_name, context)

class ViewCourseView(TemplateView):
    template_name = 'teacherportal/viewcourse.html'

    def get(self, request, courseQuery):
        
        if not request.COOKIES.get('authed_teacher'):
            # Not logged in
            return redirect('teacher-landing')

        course = dbutils.loadCourse(courseQuery)
        if course == False:
            # Course doesn't exist
            return render(request, self.template_name, {'error': 'Course could not be found.'})
        if request.COOKIES.get('authed_teacher') not in course.teacherIDs:
            # Teacher not in course, and therefore cannot view the course
            return render(request, self.template_name, {'error': 'You do not have permission to view this course.'})

        # render with list of courses
        return render(request, self.template_name, {'course': course, 'assignments': dbutils.resolveIDList(course.assignmentIDs, 'Assignment')})


class ViewAssignmentView(TemplateView):
    template_name = 'teacherportal/viewassignment.html'

    def get(self, request, assignmentQuery):
        
        if not request.COOKIES.get('authed_teacher'):
            # Not logged in
            return redirect('teacher-landing')

        assignment = dbutils.loadAssignment(assignmentQuery)
        if assignment == False:
            # Assignment doesn't exist
            return render(request, self.template_name, {'error': 'Assignment could not be found.'})
        if request.COOKIES.get('authed_teacher') not in dbutils.loadCourse(assignment.courseID).teacherIDs:
            # Teacher not in assignment's course, and therefore cannot view the assignment
            return render(request, self.template_name, {'error': 'You do not have permission to view this Assignment.'})

        # load up all submissions
        submissions = dbutils.resolveIDList(assignment.submissionIDs, 'AssignmentSubmission')

        # some iteration/formatting for displaying submissions
        for submission in submissions:
            student = dbutils.loadStudent(submission.submitterID)
            submission.displayname = student.firstName + " " + student.lastName

        return render(request, self.template_name, {'assignment': assignment, 'submissions': submissions})

class AccountView(TemplateView):
    template_name = 'teacherportal/account.html'

    def get(self, request):

        if not request.COOKIES.get('authed_teacher'):
            # Not logged in
            return redirect('teacher-landing')

        form = ChangePasswordForm()

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            teacher = dbutils.loadTeacher(request.COOKIES.get('authed_teacher'))
            current = form.cleaned_data['current']
            new1 = form.cleaned_data['new1']
            new2 = form.cleaned_data['new2']

            # make sure old password is correct and the new 2 passwords are accurate
            if hashlib.sha256(current.encode()).hexdigest() != teacher.password:
                form = ChangePasswordForm()
                return render(request, self.template_name, {'form': form, 'error': "Password incorrect."})
            elif new1 != new2:
                form = ChangePasswordForm()
                return render(request, self.template_name, {'form': form, 'error': 'Passwords did not match.'})
            else:
                # valid; change the password and log them out
                teacher.password = hashlib.sha256(new1.encode()).hexdigest()
                dbutils.saveTeacher(teacher)
                return redirect('teacher-logout')

class NewDisputeView(TemplateView):
    template_name = 'teacherportal/newdispute.html'

    def get(self, request, parentAssignment):
        
        if not request.COOKIES.get('authed_teacher'):
            # Not logged in
            return redirect('teacher-landing')

        assignment = dbutils.loadAssignment(parentAssignment)
        if assignment == False:
            # Assignment doesn't exist
            return render(request, self.template_name, {'error': 'The parent assignment could not be found.'})
        if request.COOKIES.get('authed_teacher') not in dbutils.loadCourse(assignment.courseID).teacherIDs:
            # Teacher not in assignment's course, and therefore cannot create a dispute here.
            return render(request, self.template_name, {'error': 'You do not have permission to create a dispute under this assignment.'})

        form = CreateDisputeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, parentAssignment):
        form = CreateDisputeForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['text']
            
            # create a new dispute and update all the required objects to ensure IDs are correctly networked
            firstResponse = DisputeResponse(request.COOKIES.get('authed_teacher'), message)
            dbutils.saveDisputeResponse(firstResponse)

            assignment = dbutils.loadAssignment(parentAssignment)
            course = dbutils.loadCourse(assignment.courseID)
            teachers = dbutils.resolveIDList(course.teacherIDs, 'Teacher')
            teacher = random.choice(teachers)
            
            dispute = Dispute(request.COOKIES.get('authed_teacher'), teacher.ID, [firstResponse.ID])
            dbutils.saveDispute(dispute)

            assignment.addDispute(dispute)
            dbutils.saveAssignment(assignment)

            return redirect('teacher-viewassignment', assignmentQuery=parentAssignment)


class ViewDisputeView(TemplateView):
    template_name = 'teacherportal/viewdispute.html'

    def get(self, request, disputeQuery):

        if not request.COOKIES.get('authed_teacher'):
            # Not logged in
            return redirect('teacher-landing')

        dispute = dbutils.loadDispute(disputeQuery)
        if dispute == False:
            # Dispute doesn't exist
            return render(request, self.template_name, {'error': 'Dispute could not be found.'})
        if request.COOKIES.get('authed_teacher') not in [dispute.creatorID, dispute.handlerID]:
            # Teacher not member of dispute, and therefore cannot view it
            return render(request, self.template_name, {'error': 'You do not have permission to view this Dispute.'})

        form = DisputeResponseForm()

        responses = []

        # make array of responses to display in order
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

        if 'close' in request.POST:
            # teacher wants to close the dispute
            dispute = dbutils.loadDispute(disputeQuery)
            dispute.status = False
            dbutils.saveDispute(dispute)

            form = DisputeResponseForm()

            responses = []

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

        # teacher wants to respond
        form = DisputeResponseForm(request.POST)

        if form.is_valid():
            message = form.cleaned_data['text']
            newResponse = DisputeResponse(request.COOKIES.get('authed_teacher'), message)
            dbutils.saveDisputeResponse(newResponse)

            # save response
            dispute = dbutils.loadDispute(disputeQuery)
            dispute.addResponse(newResponse)
            dbutils.saveDispute(dispute)

            form = DisputeResponseForm()

            responses = []

            # formatting for refresh
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
        return self.get(request, disputeQuery)

class StudentGradesListView(TemplateView):
    
    template_name = "teacherportal/studentgradeslist.html"

    def get(self, request):
        
        if not request.COOKIES.get('authed_teacher'):
            # Not logged in
            return redirect('teacher-landing')

        teacher = dbutils.loadTeacher(request.COOKIES.get('authed_teacher'))
        
        students = []
        studentIDs = []

        # generate array of unique student objects to display grades of
        for course in dbutils.resolveIDList(teacher.courseIDs, 'Course'):
            for student in dbutils.resolveIDList(course.studentIDs, 'Student'):
                if student.ID not in studentIDs:
                    studentIDs.append(student.ID)
                    students.append(student)

        return render(request, self.template_name, {'students': students})
        

class NewCourseView(TemplateView):
    
    template_name = "teacherportal/newcourse.html"

    def get(self, request):
        if not request.COOKIES.get('authed_teacher'):
            # Not logged in
            return redirect('teacher-landing')
        
        form = CreateCourseForm()

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            courseCode = form.cleaned_data['courseCode']
            courseName = form.cleaned_data['courseName']
            studentEmails = form.cleaned_data['studentEmails']
            teacherEmails = form.cleaned_data['teacherEmails']

            # separated by commas.
            studentEmails = studentEmails.split(",")
            teacherEmails = teacherEmails.split(",")

            course = Course(courseCode, courseName)

            authedTeacher = dbutils.loadTeacher(request.COOKIES.get('authed_teacher'))
            teacherEmails.append(authedTeacher.email)

            # add all the students
            students = []
            for email in studentEmails:
                student = dbutils.loadStudentByEmail(email)
                if student != False and student.ID not in students:
                    student.courseIDs.append(course.ID)
                    dbutils.saveStudent(student)
                    students.append(student.ID)
            teachers = []
            # add all the teachers
            for email in teacherEmails:
                teacher = dbutils.loadTeacherByEmail(email)
                if teacher != False and teacher.ID not in students:
                    teacher.courseIDs.append(course.ID)
                    dbutils.saveTeacher(teacher)
                    teachers.append(teacher.ID)

            course.studentIDs = students
            course.teacherIDs = teachers

            # save new teachers/students
            dbutils.saveCourse(course)

        return redirect('teacher-home')
            

class DeleteCourseView(TemplateView):
    
    template_name = 'teacherportal/deletecourse.html'

    def get(self, request, courseQuery):

        if not request.COOKIES.get('authed_teacher'):
            # Not logged in
            return redirect('teacher-landing')

        course = dbutils.loadCourse(courseQuery)
        if course == False:
            # Course doesn't exist
            return render(request, self.template_name, {'error': 'Course could not be found.'})
        if request.COOKIES.get('authed_teacher') not in course.teacherIDs:
            # Teacher not in course, and therefore cannot view the course
            return render(request, self.template_name, {'error': 'You do not have permission to view this course.'})

        form = ConfirmForm()

        return render(request, self.template_name, {'form': form, 'course': course})

    def post(self, request, courseQuery):
        form = ConfirmForm(request.POST)
        if form.is_valid() :
            if form.cleaned_data['text'] == "CONFIRM":
                # CONFIRMED; delete.
                course = dbutils.loadCourse(courseQuery)
                if course != False:
                    dbutils.deleteCourse(course)
                return redirect('teacher-home')
            else:
                return render(request, self.template_name, {'form': form, 'error': 'Invalid entry.'})

class NewAssignmentView(TemplateView):

    template_name = "teacherportal/newassignment.html"

    def get(self, request, parentCourse):
        if not request.COOKIES.get('authed_teacher'):
            # Not logged in
            return redirect('teacher-landing')
        
        form = CreateAssignmentForm()

        # display form
        return render(request, self.template_name, {'form': form})

    def post(self, request, parentCourse):
        # create the assignment under the parentCourse from URL
        form = CreateAssignmentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            criteria = form.cleaned_data['criteria'].split("\n")
            intensity = form.cleaned_data['intensity']

            assignment = Assignment(name, criteria, int(intensity), [], courseID=parentCourse)
            dbutils.saveAssignment(assignment)
            course = dbutils.loadCourse(parentCourse)
            course.assignmentIDs.append(assignment.ID)
            dbutils.saveCourse(course)

        return redirect('teacher-home')
            
class DeleteAssignmentView(TemplateView):
    
    template_name = 'teacherportal/deleteassignment.html'

    def get(self, request, assignmentQuery):

        if not request.COOKIES.get('authed_teacher'):
            # Not logged in
            return redirect('teacher-landing')

        assignment = dbutils.loadAssignment(assignmentQuery)
        if assignment == False:
            # Assignment doesn't exist
            return render(request, self.template_name, {'error': 'Assignment could not be found.'})
        if request.COOKIES.get('authed_teacher') not in dbutils.loadCourse(assignment.courseID).teacherIDs:
            # Teacher not in assignment's course, and therefore cannot view the assignment
            return render(request, self.template_name, {'error': 'You do not have permission to view this Assignment.'})

        form = ConfirmForm()

        return render(request, self.template_name, {'form': form, 'assignment': assignment})

    def post(self, request, assignmentQuery):
        form = ConfirmForm(request.POST)
        if form.is_valid() :
            if form.cleaned_data['text'] == "CONFIRM":
                # CONFIRMED; delete from db
                assignment = dbutils.loadAssignment(assignmentQuery)
                if assignment != False:
                    dbutils.deleteAssignment(assignment)
                return redirect('teacher-home')
            else:
                return render(request, self.template_name, {'form': form, 'error': 'Invalid entry.'})

class ViewSubmissionView(TemplateView):

    template_name = 'teacherportal/viewsubmission.html'

    def get(self, request, submissionQuery):

        if not request.COOKIES.get('authed_teacher'):
            # Not logged in
            return redirect('teacher-landing')

        submission = dbutils.loadAssignmentSubmission(submissionQuery)
        if submission == False:
            # Assignment doesn't exist
            return render(request, self.template_name, {'error': 'AssignmentSubmission could not be found.'})

        student = dbutils.loadStudent(submission.submitterID)
        displayName = student.firstName + " " + student.lastName

        disputes = []

        graded = None
        if submission.grade not in [None, False, -1]:
            graded = submission.grade
        
        # iterate through teacher's courses to locate disputes, and filter them to find the correct one
        for course in dbutils.resolveIDList(student.courseIDs, 'Course'):
            if request.COOKIES.get('authed_teacher') in course.teacherIDs:
                for assignment in dbutils.resolveIDList(course.assignmentIDs, 'Assignment'):
                    for dispute in dbutils.resolveIDList(assignment.disputeIDs, 'Dispute'):
                        if dispute.creatorID == student.ID and dispute.handlerID == request.COOKIES.get('authed_teacher') and submissionQuery in assignment.submissionIDs and dispute.ID in assignment.disputeIDs:
                            # verified that dispute is under the current assignment and teacher/student have access to it
                            disputes.append(dispute)

        # <!-- disputes array, form for grade, submission, and authorName -->

        if disputes == []:
            disputes = None

        return render(request, self.template_name, {'disputes': disputes, 'form': GradeForm(), 'submission': submission, 'authorName': displayName, 'grade': graded})

    def post(self, request, submissionQuery):
        form = GradeForm(request.POST)
        if form.is_valid():
            # update grade
            submission = dbutils.loadAssignmentSubmission(submissionQuery)
            submission.grade = int(form.cleaned_data['value'])
            dbutils.saveAssignmentSubmission(submission)
            # reload
            return self.get(request, submissionQuery)