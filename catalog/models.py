from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_login import UserMixin
import datetime

from catalog import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    name = db.Column(db.String(256))
    avatar = db.Column(db.String(256))

    def __repr__(self):
        return "{}:{}".format(self.id, self.name)


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return "{}:{}".format(self.id, self.name)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)

    __table_args__ = (db.UniqueConstraint(
        'category_id', 'name', name='_category_name_uc'),
    )

    def __repr__(self):
        return "{}:{}:{}".format(self.id, self.category_id, self.name)
