# Causes errors in python linter but works, workaround for vscode to stop spamming errors
# pylint: disable=relative-beyond-top-level
from .miscutils import generateNewID

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
    permissionLevel : None
        Dictates what functionality is available when interacting with SAPAMS. To be set by Teacher/Student classes which inherit this class.

	Methods
	-------
    sendAlert(subject, message) -> bool
        Attempts to send an email alert to the user. Returns boolean of success/failure
	'''

    def __init__(self, username, password, firstName, lastName, email, courseIDs=list(), ID=None):
        '''
		Constructor to build a User object
		
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
		bool
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