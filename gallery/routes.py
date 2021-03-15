from gallery import gallery

from flask import render_template, url_for, request

from .models import Collection, Picture

@gallery.route('/')
def index():
    return render_template('./gallery/index.html')

@gallery.route('/collections')
def collections():
    collections = Collection.query.all()
    template = './gallery/collections.html'
    return render_template(template, context=collections)


@gallery.route('/collections/<slug>')
def collection_details(slug):
    context={}
    template = './gallery/collection_details.html'

    collection = Collection.query.filter_by(slug=slug).first_or_404()
    context['collection'] = collection
    context['pictures'] = collection.pictures.all()

    return render_template(template, context=context)