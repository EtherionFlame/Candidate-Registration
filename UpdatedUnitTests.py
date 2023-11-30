import unittest
from unittest.mock import mock_open
from io import StringIO
import pymongo
from pymongo import errors
from typing import List
from main import Candidate, FileParsingPolicy, MongoDBWriter, TextFileParser, JSONFileParser, CSVFileParser, deleteCandidate
from bson.objectid import ObjectId

class TestCSVFileParser(unittest.TestCase):
   def test_parse_file(self):
      parser = CSVFileParser()
      candidates = parser.parse_file("C:\Users\garre\Downloads\wireshark-traces\TestFiles\csvtest1.csv")

      self.assertIsInstance(candidates, List)
      for candidate in candidates:
         self.assertIsInstance(candidate, Candidate)

def test_parse_file_with_invalid_file_path(self):
   parser = CSVFileParser()
   with self.assertRaises(FileNotFoundError):
      parser.parse_file("C:\Users.csv")



class TestJSONFileParser(unittest.TestCase):
   def test_parse_file(self):
      parser = JSONFileParser()
      candidates = parser.parse_file("C:\Users\garre\Downloads\wireshark-traces\TestFiles\jsontest1.json")
      
      self.assertIsInstance(candidates, List)
      for candidate in candidates:
         self.assertIsInstance(candidate, Candidate)

def test_parse_file_with_invalid_file_path(self):
   parser = JSONFileParser()
   with self.assertRaises(FileNotFoundError):
      parser.parse_file("C:\Users.json")
         

def test_parse_file_with_invalid_data(self):
   parser = TextFileParser()
   with self.assertRaises(ValueError):
      parser.parse_file("C:\Users\garre\Downloads\wireshark-traces\TestFiles\txttestfile1.txt")
         
class TestTextFileParser(unittest.TestCase):
   def test_parse_file(self):
      parser = TextFileParser()
      candidates = parser.parse_file("C:\Users\garre\Downloads\wireshark-traces\TestFiles\txttestfile1.txt")
      self.assertEqual(len(candidates), 2)
      self.assertEqual(candidates[0].getFirstName(), "Jane")
      self.assertEqual(candidates[0].getLastName(), "Doe")
      self.assertEqual(candidates[0].getDOB(), "1990-01-15")
      self.assertEqual(candidates[0].getParty(), "Independent")
      self.assertEqual(candidates[0].getParty(), "Independent")
      self.assertEqual(candidates[0].getSOC(), "123-45-6789")
      self.assertEqual(candidates[0].getPosition(), "President")

def test_parse_file_with_invalid_data(self):
   parser = TextFileParser()
   with self.assertRaises(ValueError):
      parser.parse_file("C:\Users\garre\Downloads\wireshark-traces\TestFiles\txttestfile1.txt")
      

class TestCandidate(unittest.TestCase):
  
  #This has just been created so I don't have to create a new instance of candidate for every test case.
  def createCandidate(self):
    candidate = Candidate(first_name="Jo", last_name="Bonner", DOB="1959-11-19", party="Jags", SOC="123-45-6789",position="President")

    def test_get_first_name(self):
        self.assertEqual(self.candidate.get_first_name(), "Jo")

    def test_get_last_name(self):
        self.assertEqual(self.candidate.get_last_name(), "Bonner")

    def test_get_DOB(self):
        self.assertEqual(self.candidate.get_DOB(), "1959-11-19")

    def test_get_party(self):
        self.assertEqual(self.candidate.get_party(), "Jags")
    
    def test_get_SOC(self):
        self.assertEqual(self.candidate.get_SOC(), "123-45-6789")

    def test_get_position(self):
        self.assertEqual(self.candidate.get_position(), "President")

    def test_set_parser(self):
      parser = MongoDBWriter
      self.candidate.set_parser(parser)
      self.assertEqual(self.candidate.parser, parser)

    def parse_file(self):
       file_path = "C:\Users\garre\Downloads\wireshark-traces\TestFiles\csvtest1.csv"

       self.candidate.parse_file(file_path)

       self.assertEqual(self.candidate.getFirstName(), "Jo")
       self.assertEqual(self.candidate.getLastNam(), "Bonner")
       self.assertEqual(self.candidate.getDOB(), "1959-11-19")
       self.assertEqual(self.candidate.getParty(), "Jags")
       self.assertEqual(self.candidate.getSOC(), "123-45-6789")
       self.assertEqual(self.candidate.getPosition(), "President")

    def test_CandidateUpdate(self):
       self.candidate.CandidateUpdate(first_name ="newFirst", last_name = "newLast", DOB = "2003-08-27", party="newParty", SOC = "123-45-6788")

       self.assertEqual(self.candidate.getFirstName(), "newFirst")
       self.assertEqual(self.candidate.getLastName(), "newLast")
       self.assertEqual(self.candidate.getDOB(), "2003-08-27")
       self.assertEqual(self.candidate.getParty(), "newParty")
       self.assertEqual(self.candidate.getSOC(), "123-45-6788")

#I added get_menu_choice method so I can more easily test the next definition

    def get_menu_choice(self, choice_num):
        if 1 <= choice_num <= len(self.menu_choices):
            return self.menu_choices[choice_num - 1]
        else:
            raise IndexError("choice_num is out of range")


    def test_updateMenuChoice(self):
       choiceNum=1
       currentID = 12345

       self.candidate.UpdateMenuChoices(choiceNum, currentID)

       self.assertEqual(self.candidate.get_menu_choice(choiceNum), currentID)

       with self.assertRaises(IndexError):
        self.candidate.UpdateMenuChoices(0, currentID)

    def test_valid_id():
          id = ObjectId()
          assert deleteCandidate(id) == "Candidate Deleted SUccessfully"
    def test_invalid_id():
       assert deleteCandidate('insert invalid id here') == "INvalid ID Detected"
    def test_nonexistent_id():
       id = ObjectId()
       assert deleteCandidate(id) == "No id Found"

    def test_delete_candidate():
       test_valid_id()
       test_invalid_id()
       test_nonexistent_id()

class testMongoDBWriter(unittest.TestCase):
   def test_parse_File():
      writer = MongoDBWriter()

      assert writer.parseFile("C:\Users\garre\Downloads\wireshark-traces\TestFiles\csvtest1.csv") == []

def test_write_to_mongodb():
   writer = MongoDBWriter()
   candidates = [Candidate("John", "Doe", "1990-01-01", "Republican", "123456", "U.S. Senator"),
                 Candidate("Jane", "Roe", "1985-02-02", "Democrat", "234567", "U.S. Senator")]
   
   writer.write_candidates_to_mongodb(candidates)

   for candidate in candidates:
        data = {
            "first_name": candidate.getFirstName(),
            "last_name": candidate.getLastName(),
            "DOB": candidate.getDOB(),
            "party": candidate.getParty(),
            "SOC": candidate.getSOC(),
            "position": candidate.getPosition()
        }

    ##assert collection.find_one(data) is not None
