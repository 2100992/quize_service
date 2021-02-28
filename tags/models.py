from app.models import BaseModel
from app import db

from flask import url_for

from slugify import slugify


class Tag(BaseModel):
    __tablename__ = 'tags'

    name = db.Column(db.String(100), index=True, unique=True)
    slug = db.Column(db.String(100), index=True, unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()
        self.name = self.name.lower()

    def generate_slug(self):
        self.slug = slugify(self.name)

    @property
    def url(self):
        return url_for('api_v1.tag_details', slug=self.slug, _external=True)

    def __repr__(self):
        return f'<Tag {self.name}>'
