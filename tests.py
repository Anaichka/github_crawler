import unittest
import json

from main import process_input

class TestDataType(unittest.TestCase):
    
    def test_list_input(self):
        filename = 'resources/list_input_test.json'
        with open(filename, 'r') as input:
            self.assertIsInstance(json.loads(input.read()), list)
        
    def test_dict_input(self):
        filename = 'resources/dict_input_test.json'
        with open(filename, 'r') as input:
            self.assertIsInstance(json.loads(input.read()), dict)
            
    def test_input_empty(self):
        filename = 'resources/empty_input_test.json'
        with self.assertLogs('Petlyura', level='ERROR') as cm:
            process_input(filename)
            self.assertIn("ERROR:Petlyura:JSON file can't be empty", cm.output)
        
    def test_bad_type(self):
        filename = 'resources/bad_input.txt'
        with self.assertLogs('Petlyura', level='ERROR') as cm:
            process_input(filename)
            self.assertIn("ERROR:Petlyura:Please input a valid data type. Only JSON-formatted data is allowed", cm.output)
        

if __name__ == '__main__':
    unittest.main()
    