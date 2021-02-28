from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from config import Configuration, LOGGING

import logging
import logging.config

logging.config.dictConfig(LOGGING)

app = Flask(__name__)

app.config.from_object(Configuration)
app.static_folder = app.config.get('STATIC_FOLDER', 'static')

logger = logging.getLogger('app')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from app import models
from app import routes

from tags import tags
app.register_blueprint(
    tags,
    url_pretix='/tags'
    )
from tags.models import Tag

from blog import blog
app.register_blueprint(
    blog,
    url_prefix='/blog'
    )
from blog.models import Post

from quize import quize
app.register_blueprint(
    quize,
    url_prefix='/quize'
    )

from gallery import gallery
app.register_blueprint(
    gallery,
    url_prefix='/gallery'
)
from gallery.models import Collection, Picture

from api.v1 import api_v1
app.register_blueprint(
    api_v1,
    url_prefix='/api/v1'
    )

from api.v2 import api_v2
app.register_blueprint(
    api_v2,
    url_prefix='/api/v2'
    )

@app.shell_context_processor
def make_shell_context():
    # current_user=models.User.query.first()
    return {
        'db': db,
        'User': models.User,
        'Group': models.Group,
        'Room': models.Room,
        'Post': Post,
        'Tag': Tag,
        'Collection': Collection,
        'Picture': Picture,
        'current_user': current_user,
        }
