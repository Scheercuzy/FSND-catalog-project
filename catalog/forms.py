from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import Required, DataRequired, Length, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from sqlalchemy import and_

from catalog.models import Category, Item


class CategoryForm(FlaskForm):
    name = StringField('name', validators=[
                       DataRequired(), Length(min=2, max=20)])

    def validate_name(self, name):
        category = Category.query.filter_by(
            name=name.data.capitalize()).first()
        if category:
            raise ValidationError(
                'That name is taken. Please choose a different one.')


def item_category_choices():
    return Category.query.all()


class ItemForm(FlaskForm):
    category_id = QuerySelectField(
        'Category',
        query_factory=item_category_choices,
        get_label='name',
        validators=[Required()])
    name = StringField('name', validators=[
        DataRequired(), Length(min=2, max=20)])
    description = TextAreaField('description', validators=[DataRequired()])

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
        item = Item.query.filter(and_(
            Item.name == str(self.name.data.capitalize()),
            Item.category_id == self.category_id.data.id)).first()
        if item:
            result = False
            self.name.errors.append(
                     'That name already exists in this Category.')
        return result
