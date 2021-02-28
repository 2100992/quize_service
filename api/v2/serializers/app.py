from marshmallow import Schema, fields


class UserGroupsSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str()


class UserSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    staff = fields.Bool()
    groups = fields.List(fields.Nested(UserGroupsSchema))
    # url = fields.URL()
    id = fields.Int()


class UserUpdateSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    staff = fields.Bool()
    groups = fields.List(fields.Nested(UserGroupsSchema))
    password = fields.Str()


class RoomSchema(Schema):
    name = fields.Str(required=True)
    # url = fields.URL()
