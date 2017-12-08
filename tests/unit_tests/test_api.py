import unittest
import json
import codecs
import gzip
from io import BytesIO
from base64 import b64encode
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

        self.headers = {
           'Authorization': "Basic {user}".format(user=b64encode(b"user:user").decode())
        }

    def to_gzip_data(self, input_str):
        out = BytesIO()

        with gzip.GzipFile(fileobj=out, mode="w") as f:
            f.write(input_str.encode())

        return out.getvalue()

    def test_hello(self):
        response =  self.client.get(url_for('api_v1.hello'),
                                    content_type='text')

        self.assertEqual(response.get_data(as_text=True), 'hello v1')

    def test_hello_v2(self):                                                       
        response =  self.client.get(url_for('api_v2.hello'),                    
                                    content_type='text')                        
                                                                                
        self.assertEqual(response.get_data(as_text=True), 'hello v2') 

    def test_post_json_no_required_field(self):
        response =  self.client.post(url_for('api_v1.post'),   
                                     data=json.dumps(dict(foo='bar')),
                                     content_type='application/json',
                                     headers=self.headers)

        print(response)
        self.assertEqual(response.status_code, 422)

    def test_post_json(self):                                 
        response =  self.client.post(url_for('api_v1.post'),                    
                                     data=json.dumps(dict(user_id='Alice')),          
                                     content_type='application/json',           
                                     headers=self.headers)                      
                                                                                
        self.assertEqual(response.status_code, 200)

        d = json.loads(response.get_data(as_text=True))
        self.assertEqual(d['user_id'], 'Alice')

    def test_post_json_gzip(self):              
        headers = self.headers.copy()
        headers['Content-Encoding'] = 'gzip'
                                     
        response =  self.client.post(url_for('api_v1.post'),                    
                                     data=self.to_gzip_data(json.dumps(dict(user_id='Alice'))),
                                     headers=headers)                      
                                                                                
        self.assertEqual(response.status_code, 200)                             
                                                                                
        d = json.loads(response.get_data(as_text=True))                         
        self.assertEqual(d['user_id'], 'Alice')  

if __name__ == "__main__":
    unittest.main()

