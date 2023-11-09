# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pymongo
username = "your_username"
password = "your_password"
cluster_name = "your_cluster"
database_name = "your_database"
connection_string = f"mongodb+srv://{username}:{password}@{cluster_name}.mongodb.net/{database_name}?retryWrites=true&w=majority"
class Candidate:
    def __init__(self, first_name, last_name, DOB, cand_ID, party, SOC, position):
        self.first_name = first_name
        self.last_name = last_name
        self.DOB = DOB
        self.cand_ID = cand_ID
        self.party = party
        self.SOC = SOC
        self.position = position

        def getFirstName(self):
            return self.first_name

        def getLastName(self):
            return self.last_name

        def getDOB(self):
            return self.DOB

        def getParty(self):
            return self.party

        def getSOC(self):
            return self.SOC

        def getPosition(self):
            return self.position

def registerCandidate():

    newFirstName = input("Enter your first name: ")
    newLastName = input("Enter your last name: ")
    newDOB = input("Enter your Date of Birth: ")
    newPolParty = input("Enter your political party: ")
    newSOC = input("Enter your Social Security: ")

    newCandidate = Candidate(newFirstName,newLastName,newDOB,newPolParty,newSOC)
    return newCandidate

def updateCandidate():
    print("Under Construction")
    return

def printCandidates(candidateList):
    for x in range(0,len(candidateList)):
        print("Candidate: " + str(x + 1) + "\n " +
              "------------------------")
        print("Name: " + candidateList[x].getFirstName() + " " + candidateList[x].getLastName())
        print("DOB: " + candidateList[x].getDOB())
        print("Political Party: " + candidateList[x].getParty())
        print("SOC: " + candidateList[x].getSOC() + "\n ")
        print("Office: " + candidateList[x].getPOS() + "\n")


def main():
    global inMenu
    inMenu = True
    # a dictionary to hold all valid candidates
    candidateList = []
    while(inMenu):
        print("hello welcome to the hotpatchers™ candidate registration system (>^—^)>♡ \n" +
              "Please select one of the following options \n" +
              "1. Register \n" +
              "2. Update information\n" +
              "3. Print candidate list \n" +
              "4. Exit program")
        print("-----------------------")

        userChoice = input("Menu Decision Num: ")
        choiceNum = int(userChoice)

        if choiceNum == 1:
            candidateList.append(registerCandidate())
            pause = input("Candidate registered, press enter to continue:")
        elif choiceNum == 2:
            updateCandidate()
            pause = input("Candidate updated, press enter to continue:")
        elif choiceNum == 3:
            printCandidates(candidateList)
            pause = input("list printed, press enter to continue:")
        elif choiceNum == 4:
            inMenu = False
        else:
            pause = input("invalid input, press enter to continue:")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #main()
    username = "your_username"#Replace all with credentials for MongDb
    password = "your_password"
    cluster_name = "your_cluster"
    database_name = "your_database"
    connection_string = f"mongodb+srv://{username}:{password}@{cluster_name}.mongodb.net/{database_name}?retryWrites=true&w=majority"

    # Initialize the MongoDB client and connect to a MongoDB server
    client = pymongo.MongoClient(connection_string)

    # Create or use an existing database
    db = client["candidates_database"]
    collection = db["candidates_collection"]

    candidate = Candidate("Jon","Snow",1/23/23,0,"Democrat","425-11-2222","Dog Catcher")

    candidate_data = {
        "first_name": candidate.first_name,
        "last_name": candidate.last_name,
        "DOB": candidate.DOB,
        "cand_ID": candidate.cand_ID,
        "party": candidate.party,
        "SOC": candidate.SOC,
        "position": candidate.position
    }
    result = collection.insert_one(candidate_data)

    print(candidate.first_name)
    if result.acknowledged:
        print("Candidate data inserted with ID:", result.inserted_id)

    client.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
