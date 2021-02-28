from flask import Blueprint

quize = Blueprint('quize', __name__, template_folder='templates')

from . import models
from . import routes
