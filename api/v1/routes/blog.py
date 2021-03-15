from flask import request, url_for
from flask_restful import Resource, Api

from .. import api
from ..serializers import PostSchema
from blog.models import Post


class Posts(Resource):
    def get(self):
        schema = PostSchema()
        Model = Post

        page = request.args.get('page', 1, type=int)
        items_per_page = request.args.get('ipp', 10, type=int)
        objects = Model.query.paginate(page, items_per_page, False)
        items = [schema.dump(item) for item in objects.items]

        url = url_for('api_v1.posts', _external=True)

        return {
            'posts': items,
            '_meta': {
                'pages': objects.pages,
                'page': objects.page,
                'has_next': objects.has_next,
                'has_prev': objects.has_prev,
                'next_num': objects.next_num,
                'prev_num': objects.prev_num
            },
            '_links': {
                'current_page': f"{url}?page={objects.page}",
                'first_page': f"{url}?page=1",
                'last_page': f"{url}?page={objects.pages}",
                'next_page': f"{url}?page={objects.next_num}",
                'prev_page': f"{url}?page={objects.prev_num}",
            }
        }

    def post(self):
        schema = PostSchema()
        data = request.get_json() or {}
        try:
            post_data = schema.load(data)
        except ValidationError as err:
            valid_data = err.valid_data
            messages = err.messages
            logger.error(f'valid data = {valid_data}')
            logger.error(f'invalid data = {messages}')
            return bad_request(f'valid_data={valid_data}, messages={messages}')
        else:
            bad_request_messages = []
            for key, value in post_data.items():
                attr = getattr(Post, key, None)
                if getattr(attr, 'unique', None):
                    if Post.query.filter_by(**{key: value}).first():
                        bad_request_messages.append(
                            f'please use a different {key}')
            if bad_request_messages:
                return bad_request(bad_request_messages)
            post = Post(**post_data)
            post.save()
            response = jsonify(schema.dump(post))
            response.status_code = 201
            # response.headers['Location'] = url_for(
            #     'api_v2.user_details', id=user.id)
            return response


api.add_resource(Posts, '/posts', endpoint='posts')
