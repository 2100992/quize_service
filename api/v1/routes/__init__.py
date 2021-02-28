from . import app
from . import blog
from . import squize

from api.v1 import api_v1
from flask import url_for


@api_v1.route('/')
def index():
    links = {
        'posts': url_for('api_v1.posts_list', _external=True),
        'tags': url_for('api_v1.tags_list', _external=True),
        'users': url_for('api_v1.users_list', _external=True),
        'rooms': url_for('api_v1.rooms_list', _external=True)
    }
    return links
