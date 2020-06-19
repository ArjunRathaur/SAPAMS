# pylint: disable=relative-beyond-top-level
from .miscutils import generateNewID
from .assignmentsubmission import AssignmentSubmission
from .dispute import Dispute

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
        if not isinstance(courseID, str):
            raise TypeError("Expected courseID to be of type str.")
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
