from __future__ import print_function

import logging
from logging.handlers import RotatingFileHandler
import os
import sys
import json
import base64
from flask import Flask
from flask import request
from flask import Response
from flask import stream_with_context
from flask import jsonify
from flasgger import Swagger
from functools import wraps

app = Flask(__name__)
app.debug = True

api_path = '/api/v1'

swagger = Swagger(app)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    
    golden_username = 'user'
    golden_password = 'user'

    if golden_username is None or golden_password is None:
        return False

    return username == golden_username and password == golden_password

def authenticate():
    """Sends a 401 response that enables basic auth
    """

    return Response(
        'Authenticating failed', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization

        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()

        return f(*args, **kwargs)

    return decorated

def api_error_response(code=404, message="Requested resource was not found", errors=list()):
    response = jsonify(dict(code=code, message=message, errors=errors, success=False))
    response.status_code = code

    return response

def json_required(required_fields=[]):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            errors = []

            def check_required_fields(data, fields):
                for field in fields:
                    if data.get(field) in (None, ''):
                        errors.append('{} is required.'.format(field))

            check_required_fields(request.json, required_fields)

            if errors:
                return api_error_response(code=422,
                                          message="JSON Validation Failed",
                                          errors=errors)
            return f(*args, **kwargs)

        return decorated

    return decorator

@app.route('{}/post'.format(api_path), methods=['POST'])
@requires_auth
@json_required(
    required_fields=["user_id"]
)
def post():
    """ HTTP POST demo
    ---
    consumes:
      - application/json
    parameters:
      - name: data
        in: body
        required: ["user_id"]
        schema:
          type: object
          properties:
            user_id:
              type: string               
              example: user
            greeting:
              type: string
              example: hello

    responses:
      200:
        description: echo what you post
        schema: 
          type: string
        example:
          {
            'user_id': 'user',
            'greeting': 'hello'
          }

    """
    paras = request.get_json()

    return jsonify(paras)

@app.route('{}/get'.format(api_path))
@requires_auth
def get():
    """ HTTP GET demo
    ---
    parameters:
      - name: user_id
        in: query
        type: string
        example: user
      - name: greeting
        in: query                                                       
        type: string        
        example: hello

    responses:
      200:
        description: echo args
        schema:                                                                 
          type: string                                                          
        example:                                                                
          {                                                                     
            'user_id': 'user',                                                  
            'greeting': 'hello'                                                 
          } 
    """

    return jsonify(request.args)

@app.route('{}/hello'.format(api_path))                                           
def hello():  
    return 'hello'

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=80, debug=True)
    except Exception as e:
        app.logger.error(e)



