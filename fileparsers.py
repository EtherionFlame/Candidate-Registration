from abc import ABC, abstractmethod
from typing import List
import json
import csv
from pip._internal.resolution.resolvelib.base import Candidate
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
# FileParsingStrategy interface
class FileParsingStrategy(ABC):
    @abstractmethod
    def parse_file(self, file_path: str) -> List[Candidate]:
        pass

# Concrete strategy for CSV files
class CSVFileParser(FileParsingStrategy):
    def parse_file(self, file_path: str) -> List[Candidate]:
        candidates = []
        try:
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)
                # Assuming the CSV file has a header row
                header = next(csv_reader)
                for row in csv_reader:
                    candidate = Candidate(
                        first_name=row[0],
                        last_name=row[1],
                        DOB=row[2],
                        party=row[3],
                        SOC=row[4],
                        position=row[5]
                    )
                    candidates.append(candidate)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        return candidates

#Concrete strategy for JSON files
class JSONFileParser(FileParsingStrategy):
    def parse_file(self, file_path: str) -> List[Candidate]:
        candidates = []
        try:
            with open(file_path, 'r') as file:
                json_data = file.read()
                # Assuming the JSON file contains an array of candidates
                candidates_data = json.loads(json_data)
                for candidate_data in candidates_data:
                    candidate = Candidate(
                        first_name=candidate_data.get('first_name', ''),
                        last_name=candidate_data.get('last_name', ''),
                        DOB=candidate_data.get('DOB', ''),
                        party=candidate_data.get('party', ''),
                        SOC=candidate_data.get('SOC', ''),
                        position=candidate_data.get('position', '')
                    )
                    candidates.append(candidate)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {file_path}")
        return candidates
# concrete strategy for txt files
# New concrete strategy for text files
class TextFileParser(FileParsingStrategy):
    def parse_file(self, file_path: str) -> List[Candidate]:
        candidates = []
        with open(file_path, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                if len(data) == 6:
                    candidate = Candidate(
                        first_name=data[0],
                        last_name=data[1],
                        DOB=data[2],
                        party=data[3],
                        SOC=data[4],
                        position=data[5]
                    )
                    candidates.append(candidate)
                else:
                    print(f"Invalid data format in line: {line}")

        return candidates


# Concrete strategy for MongoDB writing
class MongoDBWriter(FileParsingStrategy):

    def parse_file(self, file_path: str) -> List[Candidate]:
        #NOT CURRENTLY IMPLEMENTED OR PLANNED TO BE IMPLEMENTED
        candidates = self._read_file(file_path)
        ###return candidates

    def write_candidates_to_mongodb(self, candidates: List[Candidate]):
        # This method is specifically for writing candidates to MongoDB without reading from a file
        self._write_to_mongodb(candidates)

    def _read_file(self, file_path: str) -> List[Candidate]:
        # Use the specified parser to read data from the file
        return self.parser.parse_file(file_path)

    def _write_to_mongodb(self, candidates: List[Candidate]):
        # Implement MongoDB writing logic here
        print("Sending Data to Database:")
        uri = "mongodb+srv://ClayBarr:GenericPassword@candidateregistration.yhgqzoi.mongodb.net/?retryWrites=true&w=majority"
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client['candidates_db']
        collection = db['candidates']
        for candidate in candidates:
            data = {
                "first_name": candidate.getFirstName(),
                "last_name": candidate.getLastName(),
                "DOB": candidate.getDOB(),
                "party": candidate.getParty(),
                "SOC": candidate.getSOC(),
                "position": candidate.getPosition()
            }
            result = collection.insert_one(data)
            # Retrieve the generated MongoDB _id and store it in cand_ID
            print(result.inserted_id," Remember this as the your id")
        client.close()

# Context class (Candidate) using the strategy
class Candidate:
    def __init__(self, first_name, last_name, DOB, party, SOC, position):
        self.first_name = first_name
        self.last_name = last_name
        self.DOB = DOB

        self.party = party
        self.SOC = SOC
        self.position = position
        self.parser = None  # Added attribute to store the current strategy

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

    def set_parser(self, parser: FileParsingStrategy):
        self.parser = parser  # Set the current strategy

    def parse_file(self, file_path: str) -> List[Candidate]:
        if self.parser is not None:
            return self.parser.parse_file(file_path)
        else:
            print("Error: No parser set. Please use set_parser to set a parsing strategy.")
            return []

# Example usage
if __name__ == "__main__":
    # Create instances of parsing strategies
    file_name="C:\\Users\\roboc\\PycharmProjects\\CandidateRegistrationgFileParsers\\CandidateRegTest1 - Sheet1.csv"
    #file_name="C:\\Users\\roboc\PycharmProjects\\CandidateRegistrationgFileParsers\\txttestfile1.txt"
    assert os.path.isfile(file_name)
    csv_parser = CSVFileParser()
    json_parser = JSONFileParser()
    mongodb_writer = MongoDBWriter()
    txt_parser = TextFileParser()

    # Create an instance of the context class (Candidate)
    candidate = Candidate(first_name="John", last_name="Doe", DOB="1990-01-01",  party="Independent", SOC="123-45-6789", position="Senator")

    # Parse a CSV file using the current strategy
    csv_data = csv_parser.parse_file(file_name)
    print("CSV Data:", csv_data)

    # Switch to the JSON parsing strategy
   # candidate.set_parser(json_parser)

    # Parse a JSON file using the new strategy
    #json_data = json_parser.parse_file(file_name)
   # print("JSON Data:", json_data)

    candidate.set_parser(txt_parser)

    #txt_data = candidate.parse_file(file_name)
    #print("Text File Data:", txt_data)

    # Switch to the MongoDB writing strategy
    candidate.set_parser(mongodb_writer)

    # Parse a file and write to MongoDB using the new strategy
    #mongodb_writer.write_candidates_to_mongodb(txt_data)
    #mongodb_writer.write_candidates_to_mongodb(json_data)
    mongodb_writer.write_candidates_to_mongodb(csv_data)
