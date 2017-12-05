import unittest
import os
from flask import Flask
from flask import url_for
from flask import render_template

from app import create_app 

class TestFlaskApi(unittest.TestCase):
    template_folder = os.path.join(os.path.dirname(__file__), 'templates')

    def setUp(self):
        self.app = create_app(template_folder=self.template_folder)
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()

        @self.app.route('/large/')
        def large():
            return render_template('large.html')

    def client_get(self, ufs):
        response = self.client.get(ufs, headers=[('Accept-Encoding', 'gzip')])
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

if __name__ == "__main__":
    unittest.main()

