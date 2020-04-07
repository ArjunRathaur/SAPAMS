import uuid

def generateNewID():
    '''
    Generates a unique identifier string

    Parameters
    ----------
    None

    Returns
    -------
    str
        The hex version of the UUID.
    '''
    
    return uuid.uuid1().hex
