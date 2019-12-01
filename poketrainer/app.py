import logging

import connexion
import requests as req

from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# Create the Connexion application instance
connex_app = connexion.App(__name__, specification_dir='./')

# Get the underlying Flask app instance
flask_app = connex_app.app

# Set up the sqlalchemy database integration
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(flask_app)

# Set up the marshamallow json serialization integration
ma = Marshmallow(flask_app)

# this apparently needs to be last, otherwise the 'OperationId' handlers can't
# find the db thing they need to import from this module
connex_app.add_api('swagger.yaml')


logging.basicConfig(level=logging.INFO)


@flask_app.route('/ui/collection/')
def collection():
    pokemon = req.get(request.host_url + 'api/collection').json()
    return render_template('collection.html', pokemon=pokemon)


@flask_app.route('/ui/team/')
def team():
    pokemon = req.get(request.host_url + 'api/team').json()
    return render_template('collection.html', pokemon=pokemon)
