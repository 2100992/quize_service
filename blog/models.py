from flask import url_for

from app import db
import json

from app.models import BaseModel, Room
from tags.models import Tag

from slugify import slugify

from datetime import datetime

import collections

posts_tags = db.Table(
    'posts_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)

posts_rooms = db.Table(
    'posts_rooms',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('room_id', db.Integer, db.ForeignKey('rooms.id'))
)


class Post(BaseModel):
    __tablename__ = 'posts'

    # id = db.Column(db.Integer, prymary_key=True)
    title = db.Column(db.String(140), index=True)
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    tags = db.relationship('Tag',
                           secondary=posts_tags,
                           backref=db.backref('posts', lazy='dynamic')
                           )

    author = db.relationship('User',
                             backref=db.backref('posts', lazy='dynamic')
                             )

    room = db.relationship('Room',
                           secondary=posts_rooms,
                           backref=db.backref('posts', lazy='dynamic')
                           )

    # @property
    # def url(self):
    #     return url_for('api_v1.post_details', slug=self.slug, _external=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.generate_slug()
        self.__get_tags_from_body()
        super().save(*args, **kwargs)

    def generate_slug(self):
        time = datetime.now().strftime("%y%m%d%H%M%S")
        if self.title:
            self.slug = slugify(f'{self.title[:134]}-{time}')
        else:
            self.slug = slugify(f'No title -{time}')

    def __repr__(self):
        return f'<Post {self.title}>'

    def __str__(self):
        return self.__repr__()

    def __get_tags_from_body(self):
        # пройти по тексту и получить список слов начинающихся с '#'
        # пройти по списку, добавлять в список тегов, создать несуществующие теги
        worlds = self.body.split()
        tags = collections.Counter()
        for world in worlds:
            if world.startswith('#') and (len(world) > 1):
                tags[world[1:].lower()] += 1

        # определим сразу, что бы не читать из базы при каждом цикле
        self_tags = self.tags
        for tag_name in list(tags):
            tag = Tag.query.filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                tag.save()
            if tag not in self_tags:
                self.tags.append(tag)


class Comment(BaseModel):
    __tablename__ = 'comments'

    # id = db.Column(db.Integer, prymary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    # tags = db.relationship('Tag',
    #                        secondary=posts_tags,
    #                        backref=db.backref('comments', lazy='dynamic')
    #                        )

    author = db.relationship('User',
                             backref=db.backref('comments', lazy='dynamic')
                             )

    post = db.relationship('Post',
                           backref=db.backref('comments', lazy='dynamic')
                           )

    def __repr__(self):
        return f'<Comment {self.title}>'

    # @property
    # def url(self):
    #     return url_for('blog.comment_details', id=self.id, _external=True)
