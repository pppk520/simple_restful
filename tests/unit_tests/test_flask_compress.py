import unittest
import os
import gzip
import json
from flask import Flask
from flask import url_for
from flask import render_template
from flask import request

from app import create_app 

class TestFlaskApi(unittest.TestCase):
    template_folder = os.path.join(os.path.dirname(__file__), 'templates')
    static_folder = os.path.join(os.path.dirname(__file__), 'static')

    def setUp(self):
        self.app = create_app(template_folder=self.template_folder)
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()

        @self.app.route('/large/')
        def large():
            return render_template('large.html')

        @self.app.route('/json_gz', methods=['POST'])                           
        def post_json_gz():                                                     
            print('request = {}'.format(request))                               
            print('json = {}'.format(request.get_json()))                       
            print('files = {}'.format(request.files))                           
            print('data = {}'.format(request.data))                             
           
            json_decompress = gzip.decompress(request.data).decode('utf-8')
            print('json_decompress = {}'.format(json_decompress))
                                                                     
            return json_decompress

    def read_file(self, filepath):                                              
        with open(filepath, 'rb') as f:                                         
            return f.read() 

    def client_get(self, ufs):
        response = self.client.get(ufs, headers=[('Accept-Encoding', 'gzip')])
        self.assertEqual(response.status_code, 200)

        return response

    def client_post_gzip_request(self, ufs, gzip_request_json):                 
        response = self.client.post(ufs,                                        
                       headers={'content-encoding': 'gzip'},                    
                       data=gzip_request_json                                   
                       )                                                        
                                                                                
        self.assertEqual(response.status_code, 200)                             
                                                                                
        return response  

    def test_compress_level(self):
        self.app.config['COMPRESS_LEVEL'] = 1
        response = self.client_get('/large/')
        response1_size = len(response.data)

        self.app.config['COMPRESS_LEVEL'] = 6
        response = self.client_get('/large/')
        response6_size = len(response.data)

        self.assertNotEqual(response1_size, response6_size)

    def test_client_post_gzip_request(self):                                    
        filepath = os.path.join(self.static_folder, 'client_request.json.gz')   
        response = self.client_post_gzip_request('/json_gz', self.read_file(filepath))

        d = json.loads(response.get_data().decode('utf-8'))

        self.assertEqual(d['id'], 12345)
        self.assertEqual(d['mappings']['Alice'], '111')

if __name__ == "__main__":
    unittest.main()

