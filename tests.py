import unittest

from main import process_input

class TestDataType(unittest.TestCase):
        
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
    