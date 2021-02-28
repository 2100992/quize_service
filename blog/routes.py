from flask import render_template, request, url_for, redirect

from blog import blog

from blog.models import Post
from tags.models import Tag

@blog.route('/')
def index():
    return redirect(url_for('api_v1.index'))
