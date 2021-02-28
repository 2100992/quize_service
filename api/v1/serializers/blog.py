from marshmallow import Schema, fields
from api.v1.serializers import UserSchema


class TagSchema(Schema):
    name = fields.Str(required=True)
    slug = fields.Str()
    # url = fields.URL()


class PostSchema(Schema):
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    title = fields.Str(required=True)
    body = fields.Str(required=True)
    author = fields.Nested(UserSchema)
    # url = fields.URL()
    tags = fields.List(fields.Nested(TagSchema))


class CommentSchema(Schema):
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    title = fields.Str()
    body = fields.Str()
    author = fields.Nested(UserSchema)
    # post = fields.Nested(PostSchema)
    # url = fields.URL()


# PostSchema.comments = fields.List(fields.Nested(CommentSchema))
