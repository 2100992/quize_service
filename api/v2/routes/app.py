from flask import url_for, request
from flask import jsonify

from app.models import User, Room

from api.v2 import api_v2

from marshmallow import ValidationError

from api.v1.serializers import UserSchema, UserGroupsSchema, UserUpdateSchema
from api.v1.serializers import RoomSchema
from api.v1.serializers import PostSchema

from api.v1.errors import bad_request

import logging

logger = logging.getLogger('api_v2.routes.app')


@api_v2.route('/users', methods=['GET'])
def users_list():
    schema = UserSchema()
    Model = User

    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('ipp', 10, type=int)
    objects = Model.query.paginate(page, items_per_page, False)
    items = [schema.dump(item) for item in objects.items]

    url = url_for('api_v2.users_list', _external=True)

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


@api_v2.route('/users', methods=['POST'])
def create_user():
    user_schema = UserSchema()
    data = request.get_json() or {}
    try:
        user_data = user_schema.load(data)
    except ValidationError as err:
        valid_data = err.valid_data
        message = err.messages
        logger.error(f'valid data = {valid_data}')
        logger.error(f'invalid data = {message}')
        return bad_request(f'valid_data={valid_data}, message={message}')
    else:
        bad_request_messages = []
        for key, value in user_data.items():
            attr = getattr(User, key, None)
            if getattr(attr, 'unique', None):
                if User.query.filter_by(**{key: value}).first():
                    bad_request_messages.append(
                        f'please use a different {key}')
        if bad_request_messages:
            return bad_request(bad_request_messages)
        user = User(**user_data)
        user.save()
        response = jsonify(user_schema.dump(user))
        response.status_code = 201
        response.headers['Location'] = url_for(
            'api_v2.user_details', id=user.id)
        return response


@api_v2.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.filter(User.id == id).first_or_404()
    data = request.get_json() or {}
    user_schema = UserUpdateSchema()
    try:
        user_data = user_schema.load(data)
    except ValidationError as err:
        valid_data = err.valid_data
        message = err.messages
        logger.error(f'valid data = {valid_data}')
        logger.error(f'invalid data = {message}')
        return bad_request(f'valid_data={valid_data}, message={message}')
    else:
        bad_request_messages = []
        for key, value in user_data.items():
            attr = getattr(User, key, None)
            if getattr(attr, 'unique', None):
                if User.query.filter_by(**{key: value}).first():
                    bad_request_messages.append(
                        f'please use a different {key}')
        if bad_request_messages:
            return bad_request(bad_request_messages)
        user.update(**user_data)
        response = jsonify(user_schema.dump(user_data))
        response.status_code = 201
        response.headers['Location'] = url_for(
            'api_v2.user_details', id=user.id)
        return response


@api_v2.route('/users/<int:id>', methods=['GET'])
def user_details(id):
    user_schema = UserSchema()
    user_groups_schema = UserGroupsSchema()

    user = User.query.filter(User.id == id).first_or_404()

    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('ipp', 10, type=int)

    objects = user.comments.paginate(page, items_per_page, False)
    items = [user_groups_schema.dump(item) for item in objects.items]

    url = url_for('api_v2.user_details', _external=True, id=user.id)

    return {
        'post': user_schema.dump(user),
        'comments': items,
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


@api_v2.route('/rooms')
def rooms_list():
    schema = RoomSchema()
    Model = Room

    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('ipp', 10, type=int)
    objects = Model.query.paginate(page, items_per_page, False)
    items = [schema.dump(item) for item in objects.items]

    url = url_for('api_v2.rooms_list', _external=True)

    return {
        'rooms': items,
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


@api_v2.route('/rooms/<slug>')
def room_details(slug):
    room_schema = RoomSchema()
    post_schema = PostSchema()

    room = Room.query.filter(Room.slug == slug).first_or_404()

    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('ipp', 10, type=int)

    objects = room.posts.paginate(page, items_per_page, False)
    items = [post_schema.dump(item) for item in objects.items]

    url = url_for('api_v2.room_details', _external=True, slug=room.slug)

    return {
        'room': room_schema.dump(room),
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
