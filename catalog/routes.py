from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, logout_user

from catalog.forms import AddCategory
from catalog import db
from catalog.models import Category

url = Blueprint('url', __name__)


@url.route('/')
def index():
    return render_template('index.html', title="index")


@url.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Successfully signed out", category='info')
    return redirect(url_for('url.index'))


@url.route('/add/category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = AddCategory()
    if form.validate_on_submit():
        new_category = Category(name=form.name.data.capitalize())
        db.session.add(new_category)
        db.session.commit()
        flash("New category '{}' was successfully created".format(
            form.name.data), category='success')
        return redirect(url_for('url.index'))
    return render_template('add_category.html', form=form)
