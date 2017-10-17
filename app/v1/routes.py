import logging
import os
import sys
import json
import base64
from flask import request
from flask import Response
from flask import stream_with_context
from flask import jsonify
from flask import Blueprint

from ..common import requires_auth
from ..common import json_required

api = Blueprint('api_v1', __name__)

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
    paras = request.get_json()

    return jsonify(paras)

@api.route('/get')
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



