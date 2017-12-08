import logging
import os
import sys
import json
import base64
import gzip
from flask import stream_with_context
from flask import jsonify
from flask import request
from functools import wraps
from flask import Response

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
                # if no application/json, no checking with this function
                if not data:
                    return

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

       
            


