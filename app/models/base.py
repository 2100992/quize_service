from app import db

from datetime import datetime

from flask_login import current_user
from sqlalchemy.exc import IntegrityError

import logging

logger = logging.getLogger('app.models.base')


class CRUD:
    def save(self, *args, **kwargs):
        if self.id is None:
            db.session.add(self)
        try:
            db.session.commit()
        except IntegrityError as err:
            db.session.rollback()
            logger.error(f'db.session.commit() - {err}')
        else:
            return None

    def destroy(self, *args, **kwargs):
        db.session.delete(self)
        try:
            db.session.commit()
        except IntegrityError as err:
            db.session.rollback()
            logger.error(f'db.session.destroy() - {err}')
        else:
            pass


class BaseModel(db.Model, CRUD):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, nullable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)


class CRUDMixin:
    @classmethod
    def before_commit(cls, session):
        for obj in session.new:
            obj.created_at = datetime.now()
            obj.updated_at = datetime.now()
            # if current_user.is_authenticated:
            #     obj.author = current_user
        for obj in session.dirty:
            obj.updated_at = datetime.now()


db.event.listen(db.session, 'before_commit', CRUDMixin.before_commit)
