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
if flask_app.config['ENV'] == 'development':
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

elif flask_app.config['ENV'] == 'production':
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

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

# remove the default handlers that Flask assigns so that we get consistent
# formatting
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger('werkzeug').handlers = []
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logging.getLogger('poketrainer.api.syncs.steps').setLevel(logging.DEBUG)
logging.getLogger('poketrainer.views').setLevel(logging.DEBUG)
logging.getLogger('werkzeug').setLevel(logging.INFO)

import poketrainer.views
