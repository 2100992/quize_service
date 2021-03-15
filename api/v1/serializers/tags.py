from marshmallow import Schema, fields

class TagSchema(Schema):
    name = fields.Str(required=True)
    slug = fields.Str()