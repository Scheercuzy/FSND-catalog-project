from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_login import UserMixin
import datetime

from catalog import db


class User(UserMixin, db.Model):
    """
    Registered user information is stored in db
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    name = db.Column(db.String(256))
    avatar = db.Column(db.String(256))
    categories = db.relationship("Category", back_populates="user")
    items = db.relationship("Item", back_populates="user")

    def __repr__(self):
        return "{}:{}".format(self.id, self.name)


class OAuth(OAuthConsumerMixin, db.Model):
    """
    Registered OAuthConsumerMixin information is stored in db
    """
    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


class Category(db.Model):
    """
    Registered Category information is stored in db
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    items = db.relationship(
        "Item", back_populates="category", cascade="all, delete-orphan")
    user = db.relationship("User", back_populates="categories")

    __table_args__ = (db.UniqueConstraint(
        'user_id', 'name', name='_user_name_uc'),
    )

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def __repr__(self):
        return "{}:{}".format(self.id, self.name)


class Item(db.Model):
    """
    Registered Item information is stored in db
    """
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.relationship(
        "Category", back_populates="items")
    user = db.relationship("User", back_populates="items")

    __table_args__ = (db.UniqueConstraint(
        'category_id', 'name', name='_category_name_uc'),
    )

    @property
    def serialize(self):
        return {
            'id': self.id,
            'catergory_id': self.category_id,
            'created_date': self.created_date,
            'name': self.name,
            'description': self.description
        }

    def __repr__(self):
        return "{}:{}:{}".format(self.id, self.category_id, self.name)
