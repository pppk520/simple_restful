import unittest
from flask import Flask
from flask import url_for

from app import create_app 

class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = create_app()

        # This context can be used in two ways. 
        # Either with the with statement or by calling the push() and pop() methods.
        self.app_context = self.app.test_request_context()
        self.app_context.push()

        self.client = self.app.test_client()

    def test_hello(self):
        response =  self.client.get(url_for('api_v1.hello'),
                                    content_type='text')

        self.assertEqual(response.get_data(as_text=True), 'hello v1')

    def test_hello_v2(self):                                                       
        response =  self.client.get(url_for('api_v2.hello'),                    
                                    content_type='text')                        
                                                                                
        self.assertEqual(response.get_data(as_text=True), 'hello v2') 

if __name__ == "__main__":
    unittest.main()

