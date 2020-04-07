from classes import Assignment, AssignmentSubmission, Course, Dispute, DisputeResponse, Student, Teacher 
import pymongo

# Saving and loading setup
client = pymongo.MongoClient("mongodb+srv://SAPAMS:SAPAMS@maincluster-lo4ne.mongodb.net/test?retryWrites=true&w=majority")
db = client["objects"]

assignmentCollection = db["Assignment"]
assignmentSubmissionCollection = db["AssignmentSubmission"]
courseCollection = db["Courses"]
disputeCollection = db["Disputes"]
disputeResponseCollection = db["DisputeResponses"]
studentCollection = db["Students"]
teacherCollection = db["Teachers"]

# Database saving and loading
def saveAssignment(assignment):
    '''
    Saves an Assignment object to MongoDB.

    Parameters
    ----------
    assignment : Assignment
        The object to save.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If any passed parameters are not of the aforementioned types.
    '''
    if not isinstance(assignment, Assignment):
        raise TypeError("Attempted to save an object which was not an Assignment.")
    assignmentCollection.insert_one(vars(assignment))

def loadAssignment(ID):
    '''
    Loads an Assignment object from MongoDB.

    Parameters
    ----------
    ID : str
        The ID of the Assignment to load

    Returns
    -------
    Assignment or False
        The loaded assignment. Returns False if no document is found matching the ID.
    '''
    document = assignmentCollection.find_one({"ID": ID})
    if document == None:
        return False
    else:
        return Assignment(document["name"], document["criteria"], document["intensity"], document["dates"], document["courseID"], document["submissionIDs"], document["disputeIDs"], document["ID"])

def saveAssignmentSubmission(assignmentSubmission):
    '''
    Saves an AssignmentSubmission object to MongoDB.

    Parameters
    ----------
    assignmentSubmission : AssignmentSubmission
        The object to save.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If any passed parameters are not of the aforementioned types.
    '''
    if not isinstance(assignmentSubmission, AssignmentSubmission):
        raise TypeError("Attempted to save an object which was not an AssignmentSubmission.")
    assignmentSubmissionCollection.insert_one(vars(assignmentSubmission))

def loadAssignmentSubmission(ID):
    '''
    Loads an AssignmentSubmission object from MongoDB.

    Parameters
    ----------
    ID : str
        The ID of the AssignmentSubmission to load

    Returns
    -------
    AssignmentSubmission or False
        The loaded assignment submission. Returns False if no document is found matching the ID.
    '''
    document = assignmentSubmissionCollection.find_one({"ID": ID})
    if document == None:
        return False
    else:
        return AssignmentSubmission(document["submitterID"], document["timeStamp"], document["content"], document["grade"], document["ID"])

def saveCourse(course):
    '''
    Saves a Course object to MongoDB.

    Parameters
    ----------
    course : Course
        The object to save.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If any passed parameters are not of the aforementioned types.
    '''
    if not isinstance(course, Course):
        raise TypeError("Attempted to save an object which was not a Course.")
    courseCollection.insert_one(vars(course))

def loadCourse(ID):
    '''
    Loads a Course object from MongoDB.

    Parameters
    ----------
    ID : str
        The ID of the Course to load

    Returns
    -------
    Course or False
        The loaded course. Returns False if no document is found matching the ID.
    '''
    document = courseCollection.find_one({"ID": ID})
    if document == None:
        return False
    else:
        return Course(document["courseCode"], document["courseName"], document["studentIDs"], document["teacherIDs"], document["assignmentIDs"], document["ID"])


def saveDispute(dispute):
    '''
    Saves a Dispute object to MongoDB.

    Parameters
    ----------
    dispute : Dispute
        The object to save.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If any passed parameters are not of the aforementioned types.
    '''
    if not isinstance(dispute, Dispute):
        raise TypeError("Attempted to save an object which was not a Dispute.")
    disputeCollection.insert_one(vars(dispute))

def loadDispute(ID):
    '''
    Loads a Dispute object from MongoDB.

    Parameters
    ----------
    ID : str
        The ID of the Dispute to load

    Returns
    -------
    Dispute or False
        The loaded dispute. Returns False if no document is found matching the ID.
    '''
    document = disputeCollection.find_one({"ID": ID})
    if document == None:
        return False
    else:
        return Dispute(document["creatorID"], document["handlerID"], document["responseIDs"], document["ID"])

def saveDisputeResponses(disputeResponse):
    '''
    Saves an DisputeResponse object to MongoDB.

    Parameters
    ----------
    disputeResponse : DisputeResponse
        The object to save.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If any passed parameters are not of the aforementioned types.
    '''
    if not isinstance(disputeResponse, DisputeResponse):
        raise TypeError("Attempted to save an object which was not a DisputeResponse.")
    disputeResponseCollection.insert_one(vars(disputeResponse))


def loadDisputeResponse(ID):
    '''
    Loads a DisputeResponse object from MongoDB.

    Parameters
    ----------
    ID : str
        The ID of the DisputeResponse to load

    Returns
    -------
    DisputeResponse or False
        The loaded dispute response. Returns False if no document is found matching the ID.
    '''
    document = disputeResponseCollection.find_one({"ID": ID})
    if document == None:
        return False
    else:
        return DisputeResponse(document["authorID"], document["content"], document["ID"])


def saveStudent(student):
    '''
    Saves an Student object to MongoDB.

    Parameters
    ----------
    student : Student
        The object to save.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If any passed parameters are not of the aforementioned types.
    '''
    if not isinstance(student, Student):
        raise TypeError("Attempted to save an object which was not a student.")
    studentCollection.insert_one(vars(student))

def loadStudent(ID):
    '''
    Loads a Student object from MongoDB.

    Parameters
    ----------
    ID : str
        The ID of the Student to load

    Returns
    -------
    Student or False
        The loaded student. Returns False if no document is found matching the ID.
    '''
    document = studentCollection.find_one({"ID": ID})
    if document == None:
        return False
    else:
        return Student(document["username"], document["password"], document["firstName"], document["lastName"], document["email"], document["studentNumber"],document["courseIDs"], document["ID"])

def saveTeacher(teacher):
    '''
    Saves an Teacher object to MongoDB.

    Parameters
    ----------
    teacher : Teacher
        The object to save.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If any passed parameters are not of the aforementioned types.
    '''
    if not isinstance(teacher, Teacher):
        raise TypeError("Attempted to save an object which was not a Teacher.")
    teacherCollection.insert_one(vars(teacher))

def loadTeacher(ID):
    '''
    Loads a Teacher object from MongoDB.

    Parameters
    ----------
    ID : str
        The ID of the Teacher to load

    Returns
    -------
    Teacher or False
        The loaded teacher. Returns False if no document is found matching the ID.
    '''
    document = teacherCollection.find_one({"ID": ID})
    if document == None:
        return False
    else:
        return Teacher(document["username"], document["password"], document["firstName"], document["lastName"], document["email"], document["prefix"], document["courseIDs"], document["ID"])