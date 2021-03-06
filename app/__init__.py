from flask import Flask
from flasgger import Swagger
from .cache import cache
from flask_compress import Compress

def create_app(is_debug=True, template_folder=None):
    app = Flask(__name__, template_folder=template_folder)
    app.debug = is_debug

    cache.init_app(app)
    Compress().init_app(app)

    from .v1.routes import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1')

    from .v2.routes import api as api_2_0_blueprint                             
    app.register_blueprint(api_2_0_blueprint, url_prefix='/api/v2')  

    swag = Swagger(app)

    return app

