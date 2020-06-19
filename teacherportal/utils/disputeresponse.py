# pylint: disable=relative-beyond-top-level
from .miscutils import generateNewID

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
        if not isinstance(authorID, str):
            raise TypeError("Expected authorID to be of type str.")
        if not isinstance(content, str):
            raise TypeError("Expected content to be of type str.")

        self.authorID = authorID
        self.content = content

        # Generate Unique ID if none is passed
        if ID == None:
            self.ID = generateNewID()
        else:
            self.ID = ID