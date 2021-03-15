from marshmallow import Schema, fields
from . import TagSchema
from . import UserSchema


class CollectionsSchema(Schema):
    name = fields.Str(required=True)
    path = fields.Str()
    slug = fields.Str()
    # url = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    tags = fields.List(fields.Nested(TagSchema))
    author = fields.Nested(UserSchema)

class PictureSchema(Schema):
    name = fields.Str(required=True)
    path = fields.Str()
    collections = fields.Nested(CollectionsSchema)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    url = fields.URL()
