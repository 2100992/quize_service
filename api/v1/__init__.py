from flask import Blueprint, url_for
from flask_restful import Api, Resource

import logging
logger = logging.getLogger('api_v1.init')

api_v1 = Blueprint('api_v1', __name__)
api = Api(api_v1)

from . import routes

class index(Resource):
    def get(self):
        return {
            'collections': url_for('api_v1.collections', _external=True),
            'posts': url_for('api_v1.posts', _external=True)
            }

api.add_resource(index, '/')
