# Import the unittest module for writing and running tests
import unittest

# Import the classes and methods from the main code file (main.py)
from main import *

# Test class for file parsing strategies
class TestFileParsingStrategies(unittest.TestCase):
    # Test CSV file parsing strategy
    def test_csv_file_parser(self):
        parser = CSVFileParser()
        candidates = parser.parse_file("csvtest1.csv")
        self.assertEqual(len(candidates), 1)  # Assuming there is one valid row in the CSV file

    # Test JSON file parsing strategy
    def test_json_file_parser(self):
        parser = JSONFileParser()
        candidates = parser.parse_file("jsontest1.json")
        self.assertEqual(len(candidates), 1)  # Assuming there is one valid JSON object in the file

    # Test text file parsing strategy
    def test_text_file_parser(self):
        parser = TextFileParser()
        candidates = parser.parse_file("txttestfile1.txt")
        self.assertEqual(len(candidates), 1)  # Assuming there is one valid line in the text file

# Test class for the Candidate class
class TestCandidateClass(unittest.TestCase):
    # Test the parse_file method of the Candidate class
    def test_candidate_parse_file(self):
        # Create a Candidate object for testing
        candidate = Candidate(first_name="K", last_name="T", DOB="1990-01-01",
                              party="Independent", SOC="123-45-6789", position="Senator")

        # Set the strategy to CSVFileParser for testing
        candidate.set_parser(CSVFileParser())
        candidates = candidate.parse_file("csvtest1.csv")
        self.assertEqual(len(candidates), 1)  # Assuming there is one valid row in the CSV file

# Test class for the MongoDBWriter class
class TestMongoDBWriter(unittest.TestCase):
    # Test the write_candidates_to_mongodb method
    def test_write_candidates_to_mongodb(self):
        # Assuming MongoDB is running and accessible, and the connection details are correct
        client = MongoClient("mongodb+srv://ClayBarr:GenericPassword@candidateregistration.yhgqzoi.mongodb.net/?retryWrites=true&w=majority")
        db = client['candidates_db']
        collection = db['candidates']

        # Create a candidate object for testing
        candidate = Candidate(first_name="Test", last_name="Candidate", DOB="2000-01-01",
                              party="Test Party", SOC="987-65-4321", position="Test Position")

        # Set the strategy to MongoDBWriter for testing
        candidate.set_parser(MongoDBWriter())
        candidates = candidate.parse_file("csvtest1.csv")
        candidate.parse_file("csvtest1.csv")  # Parse the file to get the candidates
        candidate.write_candidates_to_mongodb(candidates)

        # Check if the data was inserted into MongoDB
        self.assertEqual(collection.count_documents({}), 1)

# Entry point to run the tests if this script is executed directly
if __name__ == '__main__':
    unittest.main()



