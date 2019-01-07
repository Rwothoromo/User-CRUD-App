# app/__init__.py

import os

# third-party imports
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flasgger import Swagger
from flask_cors import CORS

# local imports
from config import app_config
from app.db import db

from app.api.v1.resources.user import UserCollection, UserResource

app = Flask(__name__)
flask_config = os.environ.get('FLASK_CONFIG', 'production')
app.config.from_object(app_config[flask_config])

app.config['SWAGGER'] = {
    'swagger': '2.0',
    'title': 'User API',
    'description': "This API allows for a simple CRUD on a users DB",
    'basePath': '',
    'version': '2',
    'contact': {
        'Developer': 'Elijah Rwothoromo',
        'Profile': 'https://github.com/Rwothoromo'
    },
    'license': {
    },
    'tags': [
        {
            'name': 'User',
            'description': 'User CRUD'
        },
    ]
}

swagger = Swagger(app)

db.init_app(app)

cors = CORS(app)

# Add api Blueprint
api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix="/api/v1")


# Add resources to the API
api.add_resource(UserCollection, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')

app.register_blueprint(api_bp)
