from . import app
from . import blog
from . import squize

from api.v2 import api_v2
from flask import url_for


@api_v2.route('/')
def index():
    links = {
        'posts': url_for('api_v2.posts_list', _external=True),
        'tags': url_for('api_v2.tags_list', _external=True),
        'users': url_for('api_v2.users_list', _external=True),
        'rooms': url_for('api_v2.rooms_list', _external=True)
    }
    return links
