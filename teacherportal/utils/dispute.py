# pylint: disable=relative-beyond-top-level
from .miscutils import generateNewID

from .disputeresponse import DisputeResponse

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
        if not isinstance(creatorID, str):
            raise TypeError("Expected creatorID to be of type str.")
        if not isinstance(handlerID, str):
            raise TypeError("Expected handlerID to be of type str.")
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
    