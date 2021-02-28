import os

from flask import url_for

from app import app, db
from app.models import BaseModel

from slugify import slugify
from datetime import datetime

collections_tags = db.Table(
    'collectiond_tags',
    db.Column('collection_id', db.Integer, db.ForeignKey('collections.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)


class Collection(BaseModel):
    __tablename__ = 'collections'

    name = db.Column(db.String(140),
                     index=True,
                     unique=True,
                     nullable=False)

    path = db.Column(db.String(1024),
                     nullable=False)

    slug = db.Column(db.String(140),
                     index=True,
                     unique=True)

    parrent_collection_id = db.Column(db.Integer,
                                      db.ForeignKey('collections.id')
                                      )

    parrent_collection = db.relationship('Collection',
                                         backref=db.backref(
                                             'children_collection', lazy='dynamic')
                                         )

    author_id = db.Column(db.Integer,
                          db.ForeignKey('users.id'))

    author = db.relationship('User',
                             backref=db.backref(
                                 'collections', lazy='dynamic')
                             )

    tags = db.relationship('Tag',
                           secondary=collections_tags,
                           backref=db.backref(
                               'collections', lazy='dynamic')
                           )

    # @property
    # def url(self):
    #     return url_for('gallery.set_details', slug=self.slug)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.id:
            self.path = os.path.join(
                'media/collections', self.name)
            full_path = os.path.join(
                app.static_folder, 'media/collections', self.name)
            if not os.path.isdir(full_path):
                os.mkdir(full_path)
        if not self.slug:
            self.generate_slug()
        super().save(*args, **kwargs)

    def generate_slug(self):
        time = datetime.now().strftime("%y%m%d%H%M%S")
        if self.name:
            self.slug = slugify(f'{self.name[:134]}-{time}')
        else:
            self.slug = slugify(f'No name -{time}')

    def __repr__(self):
        return f'<Set {self.name}>'

    def __str__(self):
        return self.__repr__()


class Picture(BaseModel):
    __tablename__ = 'pictures'

    path = db.Column(db.String(1024), index=True, unique=True)
    name = db.Column(db.String(140), index=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'))

    collection = db.relationship('Collection',
                                 backref=db.backref('pictures',
                                                    lazy='dynamic'
                                                    )
                                 )

    def __init__(self, *args, path='', name='', **kwargs):
        self.path = path
        self.name = name
        if self.path and not self.name:
            self.name = os.path.split(self.path)[-1]
        super().__init__(*args, **kwargs)

    @property
    def url(self):
        return url_for('static', filename=self.path)
