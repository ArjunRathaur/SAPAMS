#-----------------------------------------------------------------------------
# Name:        Classes (classes.py)
# Purpose:     To define and document all classes to be used in the SAPAMS web app.
# Author:      Arjun Rathaur
# Created:     2020-03-22
# Updated:     2020-04-07
#-----------------------------------------------------------------------------

from miscutils import generateNewID
import dbutils

import datetime

# Email alerting imports and config
import smtplib, ssl
port = 465
email = "SAPAMSAlerting@gmail.com"
pw = "1SAPAMSAlerting!"
context = ssl.create_default_context()

class User():
    '''
	A class that allows interaction with users and their information
	
	Attributes
	----------
	username : str
		The user's login username
	password : str
		The user's password
	firstName : str
		The user's first name
	lastName : str
        The user's last name
    email : str
        The user's email address
    courseIDs : list of str
        A list of IDs of the courses the user has access to
    ID : str
        The user object's UUID.

	Methods
	-------
    sendAlert() -> None
        Attempts to send an email alert to the user
	'''

    def __init__(self, username, password, firstName, lastName, email, courseIDs=list(), ID=None):
        '''
		Constructor to build a user object
		
		If this object is not being loaded from the database, a unique ID will be generated automatically.
		
		Parameters
		----------
        username : str
            The user's login username
        password : str
            The user's password
        firstName : str
            The user's first name
        lastName : str
            The user's last name
        email : str
            The user's email address
        courseIDs : list of str, optional
            A list of IDs of the courses the user has access to
        ID : str, optional
            The user object's UUID.
        
		Raises
		------
		TypeError
			If any passed parameters are not of the aforementioned types.
		
		'''
        # Check parameter types
        if not isinstance(username, str):
            raise TypeError("Expected username to be of type str.")
        if not isinstance(password, str):
            raise TypeError("Expected password to be of type str.")
        if not isinstance(firstName, str):
            raise TypeError("Expected firstName to be of type str.")
        if not isinstance(lastName, str):
            raise TypeError("Expected lastName to be of type str.")
        if not isinstance(email, str):
            raise TypeError("Expected email to be of type str.")
        if not isinstance(courseIDs, list):
            raise TypeError("Expected courses to be of type list.")

        self.username = username
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.courseIDs = courseIDs
        self.permissionLevel = None

        # Generate Unique ID if none is passed
        if ID == None:
            self.ID = generateNewID()
        else:
            self.ID = ID

    def sendAlert(self, subject, message):
        '''
		Attempts to send an email alert to the user
		
		Parameters
		----------
        subject : str
            The subject line of the email
        message : str
            The content of the email
        
		Returns
		-------
		boolean
            True if the email succeeds, false if the email fails.

		'''
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                # Login
                server.login(email, pw)
                # Send email with correct formatting
                server.sendmail(email, self.email, "Subject: " + subject + "\n\n" + message)
            return True
        except:
            return False

class Teacher(User):
    '''
	A user class with additional information fields and methods related to teacher accounts.

    More methods will be added for "extending objects" submission.
	
	Attributes
	----------
    username : str
        The user's login username
    password : str
        The user's password
    firstName : str
        The user's first name
    lastName : str
        The user's last name
    email : str
        The user's email address
    prefix : str
        The user's preferred prefix
    courseIDs : list of str
        A list of IDs of the courses the user has access to
    ID : str
        The user object's UUID.
    permissionLevel : str
        Dictates what functionality is available when interacting with SAPAMS

	Methods
	-------
    sendAlert() -> None
        Attempts to send an email alert to the user
	'''

    def __init__(self, username, password, firstName, lastName, email, prefix, courseIDs=list(), ID=None):
        '''
		Constructor to build a teacher object
		
		If this object is not being loaded from the database, a unique ID will be generated automatically.
		
		Parameters
		----------
        username : str
            The user's login username
        password : str
            The user's password
        firstName : str
            The user's first name
        lastName : str
            The user's last name
        email : str
            The user's email address
        prefix : str
            The user's preferred prefix
        courseIDs : list of str, optional
            A list of IDs of the courses the user has access to
        ID : str, optional
            The teacher object's UUID
        
		Raises
		------
		TypeError
			If any passed parameters are not of the aforementioned types.
		
		'''
        # Check parameter types
        if not isinstance(prefix, str):
            raise TypeError("Expected prefix to be of type str.")

        super().__init__(username, password, firstName, lastName, email, courseIDs, ID)
        self.prefix = prefix
        self.permissionLevel = "ADMIN"

class Student(User):
    '''
	A user class with additional information fields and methods related to student accounts.

    More methods will be added for "extending objects" submission.
	
	Attributes
	----------
    username : str
        The user's login username
    password : str
        The user's password
    firstName : str
        The user's first name
    lastName : str
        The user's last name
    email : str
        The user's email address
    studentNumber : int
        The student's board-given student number.
    courseIDs : list of str
        A list of IDs of the courses the user has access to
    ID : str
        The user object's UUID.
    permissionLevel : str
        Dictates what functionality is available when interacting with SAPAMS

	Methods
	-------
    sendAlert() -> None
        Attempts to send an email alert to the user
    calculateAverage() -> float
        Calculates the student's overall average
	'''
    def __init__(self, username, password, firstName, lastName, email, studentNumber, courseIDs=list(), ID=None):
        '''
		Constructor to build a student object
		
		If this object is not being loaded from the database, a unique ID will be generated automatically.
		
		Parameters
		----------
        username : str
            The user's login username
        password : str
            The user's password
        firstName : str
            The user's first name
        lastName : str
            The user's last name
        email : str
            The user's email address
        studentNumber : int
            The student's board-issued student number
        courseIDs : list of str, optional
            A list of IDs of the courses the user has access to
        ID : str, optional
            The student object's UUID
        
		Raises
		------
		TypeError
			If any passed parameters are not of the aforementioned types.
		
		'''
        # Check parameter types
        if not isinstance(studentNumber, int):
            raise TypeError("Expected studentNumber to be of type int.")

        super().__init__(username, password, firstName, lastName, email, courseIDs, ID)
        self.studentNumber = studentNumber
        self.permissionLevel = "USER"

    def calculateAverage(self):
        '''
		Calculates the student's overall average

		Parameters
		----------
        None

        Returns
        -------
        float or int
            The student's overall average. Returns -1 if the user has no graded assignments.
		'''
        # variables for final division statement, which are modified as assignment grades are iterated

        total = 0
        divide = 0
        for courseID in self.courseIDs:
            for assignmentID in dbutils.loadCourse(courseID).assignmentIDs:
                for submissionID in dbutils.loadAssignment(assignmentID).submissionIDs:
                    submission = dbutils.loadAssignmentSubmission(submissionID)
                    if submission.submitterID == self.ID and submission.grade != None:
                        total += submission.grade
                        divide += 1
        if divide == 0:
            return -1
        else:
            return total/divide

# Course
class Course():
    '''
	A class with information fields and methods related to courses.
	
	Attributes
	----------
    courseCode : str or int
        The course's code
    courseName : str
        The course's name
    studentIDs : list of str
        A list of IDs of the students who have access to this course
    teacherIDs : list of str
        A list of IDs of the teachers who have access to this course
    assignmentIDs : list of str
        A list of IDs of the assignments which belong to this course.
    ID : str
        The Course object's UUID.


	Methods
	-------
    addStudent(student : Student) -> None
        Adds a student to this course
    removeStudent(student : Student) -> None
        Removes a student from this course
    addTeacher(teacher : Teacher) -> None
        Adds a teacher to this course
    removeTeacher(teacher : Teacher) -> None
        Removes a teacher from this course
    addAssignment(assignment : Assignment) -> None
        Adds an assignment to this course
    removeAssignment(assignment : Assignment) -> None
        Removes an assignment from this course
	'''

    def __init__(self, courseCode, courseName, studentIDs=list(), teacherIDs=list(), assignmentIDs=list(), ID=None):
        '''
		Constructor to build a student object
		
		If this object is not being loaded from the database, a unique ID will be generated automatically.
		
		Parameters
		----------
        courseCode : str
            The course's code
        courseName : str
            The course's
        studentIDs : list of str, optional
            A list of IDs of the students that have access to the course
        teacherIDs : list of str, optional
            A list of IDs of the teachers that have access to the course
        assignmentIDs : list of str, optional
            A list of IDs of the assignments that belond to this course
        ID : str, optional
            The Course object's UUID
        
		Raises
		------
		TypeError
			If any passed parameters are not of the aforementioned types.
		'''

        # Check parameter types
        if not isinstance(courseCode, (str, int)):
            raise TypeError("Expected courseCode to be of type str or int.")
        if not isinstance(courseName, str):
            raise TypeError("Expected courseName to be of type str.")
        if not isinstance(studentIDs, list):
            raise TypeError("Expected studentIDs to be of type list.")
        if not isinstance(teacherIDs, list):
            raise TypeError("Expected teacherIDs to be of type list.")
        if not isinstance(assignmentIDs, list):
            raise TypeError("Expected assignmentIDs to be of type list.")

        self.courseCode = str(courseCode)
        self.courseName = courseName
        self.studentIDs = studentIDs
        self.teacherIDs = teacherIDs
        self.assignmentIDs = assignmentIDs

        # Generate Unique ID if none is passed
        if ID == None:
            self.ID = generateNewID()
        else:
            self.ID = ID

    def addStudent(self, student):
        '''
		Adds a student to this course

		Parameters
		----------
        student : Student
            The Student object whose ID will be added to the course
        
        Returns
        -------
        None

		'''
        if not isinstance(student, Student):
            raise TypeError("Attempted to add a student to a course which was not of type Student.")
        self.studentIDs.append(student.ID)

    def removeStudent(self, student):
        '''
		Removes a student from this course

		Parameters
		----------
        student : Student
            The Student object whose ID will be removed from the course
        
        Returns
        -------
        None
        
		'''
        if not isinstance(student, Student):
            raise TypeError("Attempted to remove a student from a course which was not of type Student.")
        self.studentIDs.remove(student.ID)

    def addTeacher(self, teacher):
        '''
		Adds a teacher to this course

		Parameters
		----------
        teacher : Teacher
            The Teacher object whose ID will be added to the course
        
        Returns
        -------
        None

		'''
        if not isinstance(teacher, Teacher):
            raise TypeError("Attempted to add a teacher to a course which was not of type Teacher.")
        self.teacherIDs.append(teacher.ID)

    def removeTeacher(self, teacher):
        '''
		Removes a teacher from this course

		Parameters
		----------
        teacher : Teacher
            The Teacher object whose ID will be removed from the course
        
        Returns
        -------
        None
        
		'''
        if not isinstance(teacher, Teacher):
            raise TypeError("Attempted to remove a teacher from a course which was not of type Teacher.")
        self.teacherIDs.remove(teacher.ID)

    def addAssignment(self, assignment):
        '''
		Adds an assignment to this course

		Parameters
		----------
        assignment : Assignemnt
            The Assignment object whose ID will be added to the course
        
        Returns
        -------
        None

		'''
        if not isinstance(assignment, Assignment):
            raise TypeError("Attempted to add an assignment to a course which was not of type Assignment.")
        self.assignmentIDs.append(assignment.ID)

    def removeAssignment(self, assignment):
        '''
		Removes an assignment from this course

		Parameters
		----------
        assignment : Assignment
            The Assignment object whose ID will be removed from the course
        
        Returns
        -------
        None
        
		'''
        if not isinstance(assignment, Assignment):
            raise TypeError("Attempted to remove an assignment from a course which was not of type Assignment.")
        self.assignmentIDs.remove(assignment.ID)

# Assignment

class Assignment():
    '''
	A class with information fields and methods related to assignments.
	
	Attributes
	----------
    name : str
        The name of the assignment
    criteria : list of str
        The criteria for the assignment which students are being assessed on
    intensity: int
        The intensity of the assignment as rated by the creating teacher.
    dates : list of datetime
        The dates over which this Assignment spans. This is used when displaying the workload calendar to teachers during assignment planning.
    courseID : str
        The ID of the course this Assignment belongs to
    submissionIDs : list of str
        A list of IDs of the AssignmentSubmissions which belong to this Assignment.
    disputeIDs : list of str
        A list of IDs of the Disputes which belong to this Assignment
    ID : str
        This Assignment object's UUID.

	Methods
	-------
    addSubmission(submission : AssignmentSubmission) -> None
        Adds an AssignmentSubmission object's ID to this Assignment's submission list
    addDispute(dispute : Dispute) -> None
        Adds a Dispute object's ID to this Assignment's dispute list
	'''

    def __init__(self, name, criteria, intensity, dates, courseID, submissionIDs=list(), disputeIDs=list(), ID=None):
        '''
		Constructor to build an Assignment object.
		
		If this object is not being loaded from the database, a unique ID will be generated automatically.
		
		Parameters
		----------
        name : str
            The name of the assignment
        criteria : list of str
            The criteria for the assignment which students are being assessed on
        intensity: int
            The intensity of the assignment as rated by the creating teacher.
        dates : list of datetime
            The dates over which this Assignment spans. This is used when displaying the workload calendar to teachers during assignment planning.
        courseID : str
            The ID of the course this Assignment belongs to
        submissionIDs : list of str, optional
            A list of IDs of the AssignmentSubmissions which belong to this Assignment.
        disputeIDs : list of str, optional
            A list of IDs of the Disputes which belong to this Assignment
        ID : str, optional
            This Assignment object's UUID.
        
		Raises
		------
		TypeError
			If any passed parameters are not of the aforementioned types.
		'''
        # Check parameter types
        if not isinstance(name, str):
            raise TypeError("Expected name to be of type str.")
        if not isinstance(criteria, list):
            raise TypeError("Expected courseName to be of type list.")
        if not isinstance(intensity, int):
            raise TypeError("expected intensity to be of type int.")
        if not isinstance(dates, list):
            raise TypeError("Expected intensity to be of type list")
        if not isinstance(courseID, int):
            raise TypeError("Expected courseID to be of type int.")
        if not isinstance(submissionIDs, list):
            raise TypeError("Expected submissionIDs to be of type list.")
        if not isinstance(disputeIDs, list):
            raise TypeError("Expected disputeIDs to be of type list.")
        
        self.name = name
        self.criteria = criteria
        self.intensity = intensity
        self.dates = dates
        self.courseID = courseID
        self.submissionIDs = submissionIDs
        self.disputeIDs = disputeIDs

        # Generate Unique ID if none is passed
        if ID == None:
            self.ID = generateNewID()
        else:
            self.ID = ID

    def addSubmission(self, assignmentSubmission):
        '''
		Adds a submission to this assignment

		Parameters
		----------
        assignmentSubmission : AssignemntSubmission
            The AssignmentSubmission object whose ID will be added to the Assignment
        
        Returns
        -------
        None

		'''
        if not isinstance(assignmentSubmission, AssignmentSubmission):
            raise TypeError("Attempted to add a submission to an assignment which was not of type AssignmentSubmission.")
        self.submissionIDs.append(assignmentSubmission.ID)

    def addDispute(self, dispute):
        '''
		Adds a dispute to this assignment

		Parameters
		----------
        dispute : Dispute
            The Dispute object whose ID will be added to the Assignment
        
        Returns
        -------
        None

		'''
        if not isinstance(dispute, Dispute):
            raise TypeError("Attempted to add a dispute to an assignment which was not of type Dispute.")
        self.disputeIDs.append(dispute.ID)

# AssignmentSubmission
class AssignmentSubmission():
    '''
	A class with information fields and methods related to assignment submissions.
	
	Attributes
	----------
    submitterID : str
        The ID of the user who created the submission
    timeStamp : datetime
        When the assignment submission was created
    content : list of str
        Submission content (links, etc)
    grade : float or int, optional
        The grade assigned to the submission.
    ID : str
        This AssignmentSubmission object's UUID.

	Methods
	-------
    gradeAssignment(grade : float or int) -> None
        Assigns a grade to this submission
	'''

    def __init__(self, submitterID, timeStamp, content, grade=None, ID=None):
        '''
		Constructor to build an AssignmentSubmission object.
		
		If this object is not being loaded from the database, a unique ID will be generated automatically.
		
		Parameters
		----------
        submitterID : str
            The ID of the user who created the submission
        timeStamp : datetime
            When the assignment submission was created
        content : list of str
            Submission content (links, etc)
        grade : float or int, optional
            The grade assigned to the submission.
        ID : str
            This AssignmentSubmission object's UUID.

		Raises
		------
		TypeError
			If any passed parameters are not of the aforementioned types.
		'''
        # Check parameter types
        if not isinstance(submitterID, int):
            raise TypeError("Expected submitterID to be of type int.")
        if not isinstance(timeStamp, datetime.datetime):
            raise TypeError("Expected timeStamp to be of type datetime.")
        if not isinstance(grade, (float, int)):
            raise TypeError("Expected grade to be of type float or int.")
        if not isinstance(content, list):
            raise TypeError("Expected content to be of type list.")
        self.submitterID = submitterID
        self.timeStamp = timeStamp
        self.content = content
        self.grade = grade

        # Generate Unique ID if none is passed
        if ID == None:
            self.ID = generateNewID()
        else:
            self.ID = ID
    
    def gradeAssignment(self, grade):
        '''
		Assigns a grade to this submission.

		Parameters
		----------
        grade : int or float, optional
            The grade to assign to this submission.

        Returns
        -------
        None

		Raises
		------
		TypeError
			If any passed parameters are not of the aforementioned types.
		'''

        if not isinstance(grade, (float, int)):
            raise TypeError("Expected grade to be of type float or int.")
        self.grade = grade

# Dispute
class Dispute():
    '''
	A class with information fields and methods related to a dispute.
	
	Attributes
	----------
    creatorID : str
        The ID of the user who opened the dispute.
    handlerID : str
        The ID of the teacher who is handling the dispute (Generally the course's teacher.)
    responseIDs : list of str, optional
        A list of IDs of the DisputeResponses which belong to this Dispute
    status : bool
        If the dispute is open (True) or closed (False)
    ID : str
        This Dispute object's UUID.

	Methods
	-------
    addResponse(disputeResponse : DisputeResponse) -> None
        Adds a DisputeResponse's ID to this Dispute.
    closeDispute() -> None
        Closes this Dispute.
	'''

    def __init__(self, creatorID, handlerID, responseIDs=list(), status=True, ID=None):
        '''
		Constructor to build an Dispute object.
		
		If this object is not being loaded from the database, a unique ID will be generated automatically.
		
		Parameters
		----------
        submitterID : str
            The ID of the user who created the submission
        timeStamp : datetime
            When the assignment submission was created
        content : list of str
            Submission content (links, etc)
        grade : float or int, optional
            The grade assigned to the submission.
        ID : str
            This AssignmentSubmission object's UUID.

		Raises
		------
		TypeError
			If any passed parameters are not of the aforementioned types.
		'''
        # Check parameter types
        if not isinstance(creatorID, int):
            raise TypeError("Expected creatorID to be of type int.")
        if not isinstance(handlerID, int):
            raise TypeError("Expected handlerID to be of type int.")
        if not isinstance(responseIDs, list):
            raise TypeError("Expected responseIDs to be of type list.")
        if not isinstance(status, bool):
            raise TypeError("Expected status to be of type bool.")
        self.creatorID = creatorID
        self.handlerID = handlerID
        self.responseIDs = responseIDs
        self.status = status

        # Generate Unique ID if none is passed
        if ID == None:
            self.ID = generateNewID()
        else:
            self.ID = ID

    def addResponse(self, disputeResponse):
        '''
		Adds a DisputeResponse's ID to this Dispute.

		Parameters
		----------
        disputeResponse : DisputeResponse
            The DisputeResponse whose ID will be added to this Dispute.

        Returns
        -------
        None
        
		Raises
		------
		TypeError
			If any passed parameters are not of the aforementioned types.
        
		'''
        if not isinstance(disputeResponse, DisputeResponse):
            raise TypeError("Attempted to add a response to Dispute which was not of type DisputeResponse.")
        self.responseIDs.append(disputeResponse.ID)
    
    def closeDispute(self):
        '''
		Closes this dispute.

		Parameters
		----------
        None

        Returns
        -------
        None

		'''
        self.open = False
    

# DisputeResponse
class DisputeResponse():
    '''
	A class with information fields for a Dispute response.
	
	Attributes
	----------
    authorID : str
        The ID of the user who responded.
    content: str
        The content of the response.
    ID : str
        This Dispute object's UUID.

	Methods
	-------
    None

	'''
    def __init__(self, authorID, content, ID=None):
        '''
		Constructor to build an DisputeResponse object.
		
		If this object is not being loaded from the database, a unique ID will be generated automatically.
		
		Parameters
		----------
        authorID : str
            The ID of the user who responded.
        content: str
            The content of the response.
        ID : str
            This AssignmentSubmission object's UUID.

		Raises
		------
		TypeError
			If any passed parameters are not of the aforementioned types.
		'''
        # Check parameter types
        if not isinstance(authorID, int):
            raise TypeError("Expected authorID to be of type int.")
        if not isinstance(content, str):
            raise TypeError("Expected content to be of type str.")

        self.authorID = authorID
        self.content = content

        # Generate Unique ID if none is passed
        if ID == None:
            self.ID = generateNewID()
        else:
            self.ID = ID