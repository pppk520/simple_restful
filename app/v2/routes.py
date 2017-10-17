from flask import Blueprint

api = Blueprint('api_v2', __name__)

@api.route('/hello')
def hello():  
    return 'hello v2'



