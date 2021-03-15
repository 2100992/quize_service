import os

import cv2

from flask import url_for

from app import app, db
from app.models import BaseModel

from slugify import slugify
from datetime import datetime

from sqlalchemy import exc

BASE_COLLECTIONS_PATH = 'media/collections'

collections_tags = db.Table(
    'collections_tags',
    db.Column('collection_id', db.Integer, db.ForeignKey('collections.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)

pictures_collections = db.Table(
    'puctures_collections',
    db.Column('collections_id', db.Integer, db.ForeignKey('collections.id')),
    db.Column('pictures_id', db.Integer, db.ForeignKey('pictures.id'))
)


class Collection(BaseModel):
    __tablename__ = 'collections'

    name = db.Column(db.String(140),
                     index=True,
                     #  unique=True,
                     nullable=False)
    path = db.Column(db.String(1024),
                     nullable=False)
    slug = db.Column(db.String(140),
                     index=True,
                     unique=True)

    parrent_id = db.Column(db.Integer,
                           db.ForeignKey('collections.id'))
    parrent = db.relationship('Collection',
                              backref=db.backref(
                                  'children', lazy='dynamic'),
                              remote_side='Collection.id')

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User',
                             backref=db.backref(
                                 'collections', lazy='dynamic'))

    tags = db.relationship('Tag',
                           secondary=collections_tags,
                           backref=db.backref(
                               'collections', lazy='dynamic'))

    @property
    def url(self, app=''):
        if app:
            return url_for(f'{app}.collection_details', slug=self.slug)
        return url_for('gallery.collection_details', slug=self.slug, _external=True)

    @property
    def _path(self):
        return os.path.join(app.static_folder, self.path)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.path:
            if self.parrent:
                base_path = self.parrent.path
            else:
                base_path = BASE_COLLECTIONS_PATH
            self.path = os.path.join(base_path, self.name)

        if not self.name:
            self.name = os.path.split(self.path)[-1]

        if not os.path.isdir(os.path.join(app.static_folder, self.path)):
            os.makedirs(os.path.join(
                app.static_folder, self.path), exist_ok=True)

        if not self.slug:
            self.generate_slug()
        super().save(*args, **kwargs)

    def scan_dir(self):
        filesystem_path = os.path.join(app.static_folder, self.path)
        forbidden_path = []
        stopfile = 'nomedia'
        PICTURE_EXTS = ['.jpg', '.jpeg', '.png', '.bmp']

        for root, dirs, files in os.walk(filesystem_path):
            if root in forbidden_path:
                print(f'forbidden_path - {root}')
            elif stopfile in files:
                print(f'nomedia dir - {root}')
            else:
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in PICTURE_EXTS:
                        _path = os.path.join(root, file)
                        path = os.path.relpath(_path, app.static_folder)
                        picture = Picture.query.filter_by(path=path).first()
                        if not picture:
                            picture = Picture(
                                path=path,
                            )
                            picture.save()
                        picture.collections.append(self)

    def scan_db(self):
        for picture in self.pictures:
            if not os.path.isfile(picture._path):
                picture.destroy()

    def generate_slug(self):
        time = datetime.now().strftime("%y%m%d%H%M%S")
        if self.name:
            self.slug = slugify(f'{self.name[:134]}-{time}')
        else:
            self.slug = slugify(f'No name -{time}')

    def __repr__(self):
        return f'<Collection {self.name}>'

    def __str__(self):
        return self.__repr__()


class Picture(BaseModel):
    __tablename__ = 'pictures'

    path = db.Column(db.String(1024), index=True, unique=True)
    name = db.Column(db.String(140), index=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'))
    image_hash = db.Column(db.String(1024), index=True)

    collections = db.relationship('Collection',
                                  secondary=pictures_collections,
                                  backref=db.backref('pictures',
                                                     lazy='dynamic'
                                                     )
                                  )

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User',
                             backref=db.backref(
                                 'pictures', lazy='dynamic'))

    def __init__(self, *args, path='', name='', **kwargs):
        self.path = path
        self.name = name
        if self.path and not self.name:
            self.name = os.path.split(self.path)[-1]
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.image_hash:
            self.image_hash = self._hash
        super().save(*args, **kwargs)

    @property
    def url(self):
        return url_for('static', filename=self.path, _external=True)

    @property
    def _path(self):
        return os.path.join(app.static_folder, self.path)

    @property
    def _hash(self, hash_size=[8, 8]) -> str:

        image = cv2.imread(self._path)
        resized = cv2.resize(image, tuple(hash_size),
                             interpolation=cv2.INTER_AREA)
        gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        avg = gray_image.mean()
        ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)

        image_hash = ''

        for x in range(hash_size[0]):
            for y in range(hash_size[1]):
                val = threshold_image[x, y]
                if val == 255:
                    image_hash += '1'
                else:
                    image_hash += '0'
        return image_hash

    # @property
    def compare(self, another) -> int:
        h_dist = self.similar_pictures.filter_by(picture=another).first()
        h_reverse_dist = self.similar_pictures_reverse.filter_by(picture=another).first()
        if h_dist:
            return h_dist.distance
        elif h_reverse_dist:
            return h_reverse_dist.distance
        else:
            h_dist = HammingDistace(self, another)
            h_dist.save()
            return h_dist.distance


class HammingDistace(BaseModel):
    __tablename__ = 'hamming_distance'

    picture_id = db.Column(db.Integer, db.ForeignKey('pictures.id'))
    picture = db.relationship(
        'Picture',
        foreign_keys=[picture_id],
        backref=db.backref('similar_pictures', lazy='dynamic')
        )

    another_id = db.Column(db.Integer, db.ForeignKey('pictures.id'))
    another = db.relationship(
        'Picture',
        foreign_keys=[another_id],
        backref=db.backref('similar_pictures_reverse', lazy='dynamic')
    )

    distance = db.Column(db.Integer)

    def __init__(self, picture, another, *args, **kwargs):
        self.picture = picture
        self.another = another
        super().__init__(*args, **kwargs)


    def save(self, *args, **kwargs):
        try:
            self.distance = self._distance
        except Exception:
            self.distance = None
        super().save(*args, **kwargs)

    @property
    def _distance(self):
        l = len(self.picture.image_hash)
        i = 0
        count = 0
        while i < l:
            if self.picture.image_hash[i] != self.another.image_hash[i]:
                count += 1
            i += 1
        return count
