import random
import json
from miscutils import generateNewID, bubbleSortGrades, selectionSortGrades, linearSearchGrades, binarySearchGrades
import datetime


def genTestData():
  overall = []
  for _ in range(0, 15000):
    tempobject = {}
    tempID = generateNewID()
    tempobject["grade"] = random.randint(50, 100)
    tempobject["name"] = tempID
    tempobject["criteria"] = [tempID]
    tempobject["intensity"] = random.randint(0, 10)
    tempobject["dates"] = [tempID]
    tempobject["courseID"] = tempID
    tempobject["submissionIDs"] = [tempID]
    tempobject["disputeIDs"] = [tempID]
    tempobject["ID"] = tempID
    overall.append(tempobject)
  with open("data.txt", "w") as file:
    file.write(json.dumps(overall))

def loadTestData():
    with open("data.txt", "r") as file:
        return json.loads(file.read())

# genTestData()
# searchdata = sorted(loadTestData().copy(), key = lambda x: x["grade"], reverse=False)

start = datetime.datetime.now()

# bubbleSortGrades(loadTestData())
# selectionSortGrades(loadTestData())
# sorted(loadTestData().copy(), key = lambda x: x["grade"], reverse=False)


# We search for a non-existent value to get times for worst-case scenarios
# linearSearchGrades(searchdata, 101)
# print(binarySearchGrades(searchdata, 101))

end = datetime.datetime.now()

timetaken = end-start

print(timetaken)
