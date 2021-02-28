from flask import render_template, request, url_for, redirect

from quize import quize

from quize.models import *


@quize.route('/')
def index():
    return redirect(url_for('api_v1.index'))