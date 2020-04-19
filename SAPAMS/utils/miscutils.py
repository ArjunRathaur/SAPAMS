#-----------------------------------------------------------------------------
# Name:        Miscellaneous Utilities (miscutils.py)
# Purpose:     House any miscellaneous functions that may be used globally
#               but don't belong in a specific file.
# Author:      Arjun Rathaur
# Created:     2020-03-24
# Updated:     2020-04-07
#-----------------------------------------------------------------------------
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
