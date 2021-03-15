from .. import api

import urllib.parse

from gallery.models import Collection, Picture, HammingDistace

from flask import request, url_for

from flask_restful import Resource, Api

from ..serializers import CollectionsSchema, PictureSchema, SimilarPictureSchema


class Collections(Resource):
    def get(self):
        schema = CollectionsSchema()
        page = request.args.get('page', 1, type=int)
        items_per_page = request.args.get('ipp', 10, type=int)
        url = url_for('api_v1.collections', _external=True)

        objects = Collection.query.filter_by(
            parrent=None).paginate(page, items_per_page, False)

        items = [schema.dump(item) for item in objects.items]

        for item in items:
            item['url'] = urllib.parse.urljoin(url, item['slug'])

        return {
            'collections': items,
            'meta': {
                'pages': objects.pages,
                'page': objects.page,
                'has_next': objects.has_next,
                'has_prev': objects.has_prev,
                'next_num': objects.next_num,
                'prev_num': objects.prev_num
            },
            'links': {
                'current_page': f"{url}?page={objects.page}",
                'first_page': f"{url}?page=1",
                'last_page': f"{url}?page={objects.pages}",
                'next_page': f"{url}?page={objects.next_num}",
                'prev_page': f"{url}?page={objects.prev_num}",
            }
        }

    def post(self):
        pass


class CollectionDetails(Resource):
    def get(self, slug):
        schema = CollectionsSchema()
        url = url_for('api_v1.collections', _external=True)

        collection = Collection.query.filter_by(slug=slug).first_or_404()
        items = schema.dump(collection)

        items['parrent'] = schema.dump(collection.parrent)

        if items['parrent']:
            items['parrent']['url'] = urllib.parse.urljoin(
                url, items['parrent']['slug'])

        items['children'] = [schema.dump(child)
                             for child in collection.children.all()]
        for child in items['children']:
            child['url'] = urllib.parse.urljoin(url, child['slug'])

        pictures = [PictureSchema().dump(picture)
                    for picture in collection.pictures.all()]

        return {
            'collection': items,
            'pictures': pictures
        }

    def post(self):
        pass


class PictureDetails(Resource):
    def get(self, id):
        schema = PictureSchema()

        picture = Picture.query.filter_by(id=id).first_or_404()
        similar_pictures = picture.similar_pictures.union(
            picture.similar_pictures_reverse).order_by(HammingDistace.distance).all()

        return {
            'picture': schema.dump(picture),
            'similar_picture': [SimilarPictureSchema().dump(picture) for picture in similar_pictures]
        }

    def post(self, id):
        pass


api.add_resource(Collections, '/gallery/', endpoint='gallery')
api.add_resource(Collections, '/gallery/collections/', endpoint='collections')
api.add_resource(CollectionDetails, '/gallery/collections/<string:slug>/',
                 endpoint='collection_details')
api.add_resource(PictureDetails, '/gallery/pictures/<int:id>',
                 endpoint='pictere_details')
