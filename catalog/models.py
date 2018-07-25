from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_login import UserMixin

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
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)

    __table_args__ = tuple(db.UniqueConstraint(
        'name', 'category_id',
        name='item_name_category_unique_constraint'))

    def __repr__(self):
        return "{}:{}:{}".format(self.id, self.category_id, self.name)
