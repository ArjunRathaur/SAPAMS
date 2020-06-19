# pylint: disable=relative-beyond-top-level
from .user import User
from . import dbutils

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
		Constructor to build a Student object
		
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
                    if submission != False and submission.submitterID == self.ID and submission.grade != None and submission.grade != -1:
                        total += submission.grade
                        divide += 1
        if divide == 0:
            return -1
        else:
            return total/divide
