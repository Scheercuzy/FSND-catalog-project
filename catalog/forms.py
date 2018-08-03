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
        """Checks if the same user and category name exists"""
        category = Category.query.filter(
            Category.name == name.data.capitalize(),
            Category.user_id == name.current_user_id).first()

        if category:
            raise ValidationError(
                'That name is taken. Please choose a different one.')


class ItemForm(FlaskForm):
    category_id = QuerySelectField(
        'Category',
        get_label='name',
        validators=[Required()])
    name = StringField('name', validators=[
        DataRequired(), Length(min=2, max=20)])
    description = TextAreaField('description', validators=[DataRequired()])

    def validate(self):
        """Validates the entire form. It checks if there is item_name and
        category_id pair exists before validating the form. when editing the
        item, it does the same check but ignores the item_id of the item
        currently being editted because it could have the same name"""

        if not FlaskForm.validate(self):
            return False
        result = True

        if hasattr(self, 'editting_item_id'):
            item = Item.query.filter(
                Item.name == self.name.data.capitalize(),
                Item.id != self.editting_item_id
                ).first()
        else:
            item = Item.query.filter(and_(
                Item.name == str(self.name.data.capitalize()),
                Item.category_id == self.category_id.data.id)).first()

        if item:
            result = False
            self.name.errors.append(
                'That name already exists in this Category.')
        return result
