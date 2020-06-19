# pylint: disable=relative-beyond-top-level
from .miscutils import generateNewID
from .student import Student
from .teacher import Teacher
from .assignment import Assignment

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
		Constructor to build a Course object
		
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
