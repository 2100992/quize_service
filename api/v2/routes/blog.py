from flask import request, url_for

from blog.models import Post
from tags.models import Tag

from api.v2 import api_v2
from api.v2.serializers import PostSchema, TagSchema, CommentSchema


@api_v2.route('/posts/')
def posts_list():
    schema = PostSchema()
    Model = Post

    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('ipp', 10, type=int)
    objects = Model.query.paginate(page, items_per_page, False)
    items = [schema.dump(item) for item in objects.items]

    url = url_for('api_v2.posts_list', _external=True)

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


@api_v2.route('/posts/<slug>')
def post_details(slug):
    post_schema = PostSchema()
    comment_schema = CommentSchema()
    post = Post.query.filter(Post.slug == slug).first_or_404()

    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('ipp', 10, type=int)

    objects = post.comments.paginate(page, items_per_page, False)
    items = [comment_schema.dump(item) for item in objects.items]

    url = url_for('api_v2.post_details', _external=True, slug=post.slug)

    return {
        'post': post_schema.dump(post),
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


@api_v2.route('/tags/')
def tags_list():
    schema = TagSchema()
    Model = Tag

    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('ipp', 10, type=int)
    objects = Model.query.paginate(page, items_per_page, False)
    items = [schema.dump(item) for item in objects.items]

    url = url_for('api_v2.tags_list', _external=True)

    return {
        'tags': items,
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


@api_v2.route('/tags/<slug>')
def tag_details(slug):
    post_schema = PostSchema()
    tag_schema = TagSchema()
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    posts = [post_schema.dump(post) for post in tag.posts]
    return {
        'posts': posts,
        'tag': tag_schema.dump(tag)
    }
