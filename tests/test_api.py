import unittest
import requests
import json

class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.server = 'http://localhost/api/v1/'


    def test_hello(self):
        response = requests.get(self.server + 'hello')
        self.assertEqual(response.text, 'hello')

if __name__ == "__main__":
    unittest.main()

