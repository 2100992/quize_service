from app import db
from app.models import BaseModel
from slugify import slugify

from flask import url_for

room_staff = db.Table(
    'room_staff',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('room_id', db.Integer, db.ForeignKey('rooms.id'))
)

room_member = db.Table(
    'room_member',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('room_id', db.Integer, db.ForeignKey('rooms.id'))
)


class Room(BaseModel):
    __tablename__ = 'rooms'

    name = db.Column(db.String(140), index=True)
    slug = db.Column(db.String(140), index=True)
    descriptions = db.Column(db.Text)

    staff = db.relationship('User',
                            secondary=room_staff,
                            backref=db.backref('staff_in_rooms', lazy='dynamic')
                            )

    members = db.relationship('User',
                              secondary=room_member,
                              backref=db.backref('member_in_rooms', lazy='dynamic')
                              )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        self.slug = slugify(self.name)

    def __repr__(self):
        return f'<Room {self.name}>'

    @property
    def url(self):
        return url_for('api_v1.room_details', slug=self.slug, _external=True)
