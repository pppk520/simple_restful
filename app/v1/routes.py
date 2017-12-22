import logging
import os
import sys
import json
import base64
import gzip
from flask import request
from flask import Response
from flask import stream_with_context
from flask import jsonify
from flask import Blueprint

from ..common import requires_auth
from ..common import json_required

mylogger = logging.getLogger('mylog')

api = Blueprint('api_v1', __name__)

def decompress_data(alg, data):
    if alg == 'gzip':
        return gzip.decompress(request.data).decode('utf-8')

def get_request_json(request):
    ''' Might be compressed or not
    '''

    alg = request.headers.get('Content-Encoding')
    decompressed_data = decompress_data(alg, request.data)

    # expects to be compressed json string 
    if decompressed_data:
        return json.loads(decompressed_data)

    return request.get_json()

@api.route('/post', methods=['POST'])
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
    
    paras = get_request_json(request)

    mylogger.info(paras)

    return jsonify(paras)

@api.route('/echo', methods=['POST'])
@requires_auth
def echo():
    paras = get_request_json(request)                                           
            
    return jsonify(paras) 

@api.route('/get', methods=['GET'])
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

@api.route('/hello')
def hello():  
    return 'hello v1'



