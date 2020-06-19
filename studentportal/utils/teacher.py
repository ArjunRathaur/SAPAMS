# pylint: disable=relative-beyond-top-level
from .user import User

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
		Constructor to build a Teacher object
		
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
