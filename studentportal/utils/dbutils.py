#-----------------------------------------------------------------------------
# Name:        Database Utilities (dbutils.py)
# Purpose:     Make saving/loading classes in classes.py to MongoDB easier
# Author:      Arjun Rathaur
# Created:     2020-03-29
# Updated:     2020-04-07
#-----------------------------------------------------------------------------

# import classes for saving/loading
# pylint: disable=relative-beyond-top-level, undefined-variable
from .assignment import Assignment
from .assignmentsubmission import AssignmentSubmission
from .course import Course
from .dispute import Dispute
from .disputeresponse import DisputeResponse
from .student import Student
from .teacher import Teacher

# Saving and loading setup
import pymongo
client = pymongo.MongoClient("mongodb+srv://SAPAMS:SAPAMS@maincluster-lo4ne.mongodb.net/test?retryWrites=true&w=majority")
db = client["objects"]

assignmentCollection = db["Assignments"]
assignmentSubmissionCollection = db["AssignmentSubmissions"]
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
    if loadAssignment(assignment.ID) == False:
        assignmentCollection.insert_one(vars(assignment))
    else:
        assignmentCollection.replace_one({"ID": assignment.ID}, vars(assignment))

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
    if loadAssignmentSubmission(assignmentSubmission.ID) == False:
        assignmentSubmissionCollection.insert_one(vars(assignmentSubmission))
    else:
        assignmentSubmissionCollection.replace_one({"ID": assignmentSubmission.ID}, vars(assignmentSubmission))

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
    if loadCourse(course.ID) == False:
        courseCollection.insert_one(vars(course))
    else:
        courseCollection.replace_one({"ID": course.ID}, vars(course))

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
    if loadDispute(dispute.ID) == False:
        disputeCollection.insert_one(vars(dispute))
    else:
        disputeCollection.replace_one({"ID": dispute.ID}, vars(dispute))

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
        return Dispute(document["creatorID"], document["handlerID"], document["responseIDs"], document['status'], document["ID"])

def saveDisputeResponse(disputeResponse):
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
    if loadDisputeResponse(disputeResponse.ID) == False:
        disputeResponseCollection.insert_one(vars(disputeResponse))
    else:
        disputeResponseCollection.replace_one({"ID": disputeResponse.ID}, vars(disputeResponse))


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
    if loadStudent(student.ID) == False:
        studentCollection.insert_one(vars(student))
    else:
        studentCollection.replace_one({"ID": student.ID}, vars(student))

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
    if loadTeacher(teacher.ID) == False:
        teacherCollection.insert_one(vars(teacher))
    else:
        teacherCollection.replace_one({"ID": teacher.ID}, vars(teacher))

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

def resolveIDList(listToResolve, classType):
    '''
    Attempts to resolve a list of IDs and return a list of classes that match said IDs.

    When dealing with some classes, for example Courses, certain attributes are simply ID lists to create associations between objects rather than lists of objects.

    Parameters
    ----------
    listToResolve : list
        The list of IDs to resolve.
    classType : str
        The class type that the IDs in the listToResolve are for.
        Available types are 'Assignment', 'AssignmentSubmission', 'Course', 'Dispute', 'DisputeResponse', 'Student', and 'Teacher'.

    Returns
    -------
    List of objects
        The resolved list of objects of class specified in parameter classType.

    Raises
    ------
    KeyError
        If an object cannot be found for any ID in the listToResolve.
    TypeError
        If either parameter is not of the aforementioned type
    TypeError
        If the classType parameter does not specify a valid type.
    '''
    
    # Parameter checks
    if not isinstance(listToResolve, list):
        raise TypeError("Attempted to resolve a parameter which is not a list.")
    if not isinstance(classType, str):
        raise TypeError("Invalid classType specified (expected a string)")

    # Now we actually try resolving the IDs
    resolvedList = []
    if classType == "Assignment":
        for ID in listToResolve:
            result = loadAssignment(str(ID))
            if not result:
                raise KeyError("Could not find an Assignment object with ID " + str(ID))
            resolvedList.append(result)
    elif classType == "AssignmentSubmission":
        for ID in listToResolve:
            result = loadAssignmentSubmission(str(ID))
            if not result:
                raise KeyError("Could not find an AssignmentSubmission object with ID " + str(ID))
            resolvedList.append(result)
    elif classType == "Course":
        for ID in listToResolve:
            result = loadCourse(str(ID))
            if not result:
                raise KeyError("Could not find a Course object with ID " + str(ID))
            resolvedList.append(result)
    elif classType == "Dispute":
        for ID in listToResolve:
            result = loadDispute(str(ID))
            if not result:
                raise KeyError("Could not find a Dispute object with ID " + str(ID))
            resolvedList.append(result)
    elif classType == "DisputeResponse":
        for ID in listToResolve:
            result = loadDisputeResponse(str(ID))
            if not result:
                raise KeyError("Could not find a DisputeResponse object with ID " + str(ID))
            resolvedList.append(result)
    elif classType == "Student":
        for ID in listToResolve:
            result = loadStudent(str(ID))
            if not result:
                raise KeyError("Could not find a Student object with ID " + str(ID))
            resolvedList.append(result)
    elif classType == "Teacher":
        for ID in listToResolve:
            result = loadTeacher(str(ID))
            if not result:
                raise KeyError("Could not find a Teacher object with ID " + str(ID))
            resolvedList.append(result)
    else:
        raise TypeError("Invalid classType specified!")
    return resolvedList

def loadStudentByEmail(email):
    '''
    Loads a Student object from MongoDB by email query.

    Parameters
    ----------
    email : str
        The email of the Student to load

    Returns
    -------
    Student or False
        The loaded student. Returns False if no document is found matching the ID.
    '''
    document = studentCollection.find_one({"email": email})
    if document == None:
        return False
    else:
        return Student(document["username"], document["password"], document["firstName"], document["lastName"], document["email"], document["studentNumber"],document["courseIDs"], document["ID"])

def loadTeacherByEmail(email):
    '''
    Loads a Teacher object from MongoDB by email query.

    Parameters
    ----------
    email : str
        The email of the Teacher to load

    Returns
    -------
    Teacher or False
        The loaded Teacher. Returns False if no document is found matching the ID.
    '''
    document = teacherCollection.find_one({"email": email})
    if document == None:
        return False
    else:
        return Teacher(document["username"], document["password"], document["firstName"], document["lastName"], document["email"], document["prefix"], document["courseIDs"], document["ID"])

