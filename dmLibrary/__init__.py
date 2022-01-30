import os

from flask import Flask, jsonify, Response

from flask_cors import CORS
from flask_migrate import Migrate

from dmLibrary.config import config
from dmLibrary.database.models import *



migrate = Migrate()
class JSONResponse(Response):
    """ Customized Flask Response class for native JSON returns """
    @classmethod
    def force_type(cls, rv, environ=None):
        """ Custom method for JSON returns """
        if isinstance(rv, (dict, list)):
            rv = jsonify(rv)
        if isinstance(rv, set):
            rv = jsonify(sorted(list(rv)))
        return super(JSONResponse, cls).force_type(rv, environ)

def create_app(cfg=None):
    """ Define the app object and instantiate context """
    # Instantiate app object
    # app = Flask(__name__,static_folder=static_dir, template_folder=template_dir, static_url_path='')
    app = Flask(__name__)
    app.jinja_options = {}
    
    if cfg:
        app.config.update(cfg)
    else:
        app.config.update(config)
        
    app.response_class = JSONResponse
    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise ValueError("SQLALCHEMY_DATABASE_URI cannot be found in config. "
        "please environment variable 'DATABASE_URI'")


    app.logger.debug("SQLALCHEMY_DATABASE_URI:{}".format(app.config['SQLALCHEMY_DATABASE_URI']))
    # Instantiate CORS
    CORS(app)
    # api routes

    from dmLibrary.api.v1 import bp as api
    app.register_blueprint(api, url_prefix='/api/v1')

    # UI routes
    from dmLibrary.ui import bp as ui
    app.register_blueprint(ui, url_prefix='/')

    from dmLibrary.database import db, ma

    # attach app to migrate object
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)


    app.app_context().push()
    
    return app