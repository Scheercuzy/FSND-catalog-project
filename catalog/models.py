from catalog import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.username}"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.id}:{self.name}"


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
        return f"{self.id}:{self.category_id}:{self.name}"
