import logging
import os

import connexion

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Create the Connexion application instance
connex_app = connexion.App(__name__, specification_dir='./')

# Get the underlying Flask app instance
flask_app = connex_app.app

# Default to HTTPS (OAuth things require it, and no harm in using it generally)
# c.f https://stackoverflow.com/a/37842465
class ForceHTTPS(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['wsgi.url_scheme'] = 'https'
        return self.app(environ, start_response)

flask_app.wsgi_app = ForceHTTPS(flask_app.wsgi_app)

# Set up the sqlalchemy database integration
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(flask_app)

# Set up the Fitbit API credentials
flask_app.config.update(
    FITBIT_CLIENT_ID=os.getenv('FITBIT_CLIENT_ID'),
    FITBIT_CLIENT_SECRET=os.getenv('FITBIT_CLIENT_SECRET'),
    FITBIT_REFRESH_TOKEN=None)

# Set up the marshamallow json serialization integration
ma = Marshmallow(flask_app)

# this apparently needs to be last, otherwise the 'OperationId' handlers can't
# find the db thing they need to import from this module
connex_app.add_api('swagger.yaml')

logging.basicConfig(level=logging.INFO)

import poketrainer.views
