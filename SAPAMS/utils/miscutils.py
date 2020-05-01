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

# Sorting bubble/selection for AssignmentSubmissions, sorting is done based on 'grade' attribute values.

def bubbleSortGrades(assignmentSubmissions):
    '''
    Sorts the given array by grade attribute using the bubble sort algorithm.

    Parameters
    ----------
    assignmentSubmissions : list of AssignmentSubmissions
        The array to sort

    Returns
    -------
    list of AssignmentSubmissions
        The sorted array.
    '''
    # assignmentSubmission.grade is the attribute we're sorting by
    for i in range(0, len(assignmentSubmissions)-1):
        # we have to sort each data value starting from index 0, this gives us all the indexes in the list given
        for v in range(0, len(assignmentSubmissions)-i-1):
            # we add -i because the last item in the list is already sorted; going over it again would be redundant and inefficient.
            if assignmentSubmissions[v].grade > assignmentSubmissions[v+1].grade:
                temp = assignmentSubmissions[v]
                assignmentSubmissions[v] = assignmentSubmissions[v+1]
                assignmentSubmissions[v+1] = temp
    return assignmentSubmissions


def selectionSortGrades(assignmentSubmissions):
    '''
    Sorts the given array by grade attribute using the selection sort algorithm.

    Parameters
    ----------
    assignmentSubmissions : list of AssignmentSubmissions
        The array to sort

    Returns
    -------
    list of AssignmentSubmissions
        The sorted array.
    '''
    # assignmentSubmission.grade is the attribute we're sorting by
    for i in range(0, len(assignmentSubmissions)-1):
        # iterate over each item in the array; 0 through length of assignmentSubmissions - 1
        minIndex = i # init minIndex so we can update it as we iterate
        for v in range (i+1, len(assignmentSubmissions)):
            # goes over values that have not yet been sorted; again, to prevent comparing already sorted values again
            if assignmentSubmissions[v].grade < assignmentSubmissions[minIndex].grade:
                # compare; if current assignmentSubmissions value is less than our minindex value, we update it
                minIndex = v
    if minIndex != i:
        # if the value needs to be moved, we swap it to its correct position
        temp = assignmentSubmissions[i]
        assignmentSubmissions[i] = assignmentSubmissions[minIndex]
        assignmentSubmissions[minIndex] = temp
    return assignmentSubmissions

def linearSearchGrades(assignmentSubmissions, query):
    '''
    Searches the given array for a grade matching the query using the linear search algorithm..

    Parameters
    ----------
    assignmentSubmissions : list of AssignmentSubmissions
        The array to search
    query : int
        The query for the search

    Returns
    -------
    int
        The index of the query in the given array. Returns -1 if query not found in array.
    '''
    # assignmentSubmission.grade is the attribute we're sorting by
    for i, submission in enumerate(assignmentSubmissions):
        # iterate all values in array with indexes so we can return the correct one
        if submission.grade == query:
            # match found
            return i
    return -1 # query not found

def binarySearchGrades(assignmentSubmissions, query):
    '''
    Searches the given array for a grade matching the query using the binary search algorithm..

    Parameters
    ----------
    assignmentSubmissions : list of AssignmentSubmissions
        The array to search
    query : int
        The query for the search

    Returns
    -------
    int
        The index of the query in the given array. Returns -1 if query not found in array.
    '''
    # set up our upper and lower bounds
    low = 0
    high = len(assignmentSubmissions) - 1

    # create a loop that keeps iterating until we find our value, which will be when high is above low
    while low <= high:
        midpoint = (low + high) // 2 # floor division ensures we always get an integer
        if assignmentSubmissions[midpoint].grade < query:
            # move to upper side of midpoint
            low = midpoint + 1
        elif assignmentSubmissions[midpoint].grade > query:
            # move to lower side of midpoint
            high = midpoint - 1
        else:
            # midpoint is the value we are querying
            return midpoint
    
    return -1 # query not found


'''
Sorting/Searching Computational Complexity Analysis
---------------------------------------------------

**NOTE**: For 5MB+ of data in the testing, the request quantity would be too large for my MongoDB Atlas to handle (cloud services result in large delays when calling thousands 
of documents), so I generated a list of 15,000 dictionaries and sorted it for testing. Two trials were conducted for two different datasets. The file used to generate the data
and any results in this comment is testgen.py.

Bubble sort has two loops that iterate the inputted list (they are nested, so they multiply n elements x n elements), so it runs in O(n^2) time.
Empirical data: sorting data.txt took 37.799s and 40.303s

Selection sort also has two nested loops that iterate the inputted list, so it runs in O(n^2) time
Empirical data: sorting data.txt took 19.714s and 19.610s
The reason this method takes less time than bubble sort is that bubble sort swaps significantly more elements than selection sort, due to the nature of the algorithm. These
modifications to list values take more computational power and time.

The reason that these methods are slower than Python's .sorted() method is because of the algorithm Python uses, called "Timsort". The computational
complexity of this algorithm is O(nlogn), which is significantly smaller than O(n^2). 
Empirical data: sorting data.txt took 1.003s and 0.095s

Linear search iterates the array once without nested loops, so in the worst case scenario it runs in O(n) time
Empirical data: searching took 0.080s and 0.072s

Binary search is a much more efficient method of searching an array, since it halves the search space with almost each iteration. This reducing quantity
of search space (n becomes n/2 becomes n/4 becomes n/8) can be modelled by a logarithmic function, and since we drop multiplicative constants when doing complexity analysis, we conclude
that binary search runs in O(log₂n). 
Empirical data: searching took <0.001s


Video Question Answers
----------------------
=> What do you notice about the searches that have the thin bars vs. those with the thicker bars?
    The sorting algorithms with thin bars are much quicker than the ones with thicker bars. Another trend I noticed is that the algorithms with thinner bars 
    break up the data into smaller sections and sort those out before creating a final sorted dataset.

=> Why would someone make this video?
    This video was created to show with visuals and audio how 15 different sorting algorithms function. It could have been made for educational purposes, or it could have been
    made because someone likes how sorting algorithms can be represented with visuals and audio.

=> Could this video be skewed to show something that is incorrect? How so?
    Absolutely; the description of the video states that speed and number of items is modified based on each algorithm's complexity, and that can impact how each algorithm's
    efficiency is conveyed to the audience. For example, the bubble sort algorithm has a much smaller dataset to sort when compared to the radix sort algorithms.
    Even though radix sorting is much more efficient, it takes longer in the video when compared to bubble sorting.

'''