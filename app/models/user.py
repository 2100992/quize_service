from app import db
from app import login

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from .base import BaseModel


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


users_groups = db.Table(
    'users_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
)


class User(UserMixin, BaseModel):
    __tablename__ = 'users'

    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    staff = db.Column(db.Boolean, default=False)

    groups = db.relationship('Group',
                             secondary=users_groups,
                             backref=db.backref('users', lazy='dynamic')
                             )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('password'):
            self.set_password(kwargs['password'])

    def __repr__(self) -> str:
        return f'<User_{self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if attr == 'password':
                self.set_password(value)
            else:
                setattr(self, attr, value)
        self.save()


class Group(BaseModel):
    __tablename__ = 'groups'

    name = db.Column(db.String(140), index=True, unique=True)
    description = db.Column(db.Text)

    def __repr__(self) -> str:
        return f'<Group {self.name}>'
