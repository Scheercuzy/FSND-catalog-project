from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, ValidationError

from catalog.models import Category


class AddCategory(FlaskForm):
    name = StringField('name', validators=[
                       DataRequired(), Length(min=2, max=20)])

    def validate_name(self, name):
        category = Category.query.filter_by(
            name=name.data.capitalize()).first()
        if category:
            raise ValidationError(
                'That name is taken. Please choose a different one.')
