import datetime

# pylint: disable=relative-beyond-top-level
from .miscutils import generateNewID

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

    def __init__(self, submitterID, timeStamp, content, grade=-1, ID=None):
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
        if not isinstance(submitterID, str):
            raise TypeError("Expected submitterID to be of type str.")
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
        self.grade = int(grade) 
        # we want to store grades as whole percentage values, 
        # so we don't have large amounts of leading/trailing decimals 
        # from floating point round errors