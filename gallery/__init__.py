from flask import Blueprint

gallery = Blueprint('gallery', __name__, template_folder='templates', static_folder='static')

from . import models
from . import routes