from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, logout_user

from catalog.forms import AddCategory, AddItem
from catalog import db
from catalog.models import Category, Item

url = Blueprint('url', __name__)


@url.route('/')
def index():
    catergories = Category.query.all()
    items = Item.query.all()
    return render_template(
        'index.html',
        title="index",
        categories=catergories,
        items=items,
        category_id=None)


@url.route('/item/<int:item_id>', methods=['GET'])
def item_detail(item_id):
    item = Item.query.filter(Item.id == item_id).first()
    if not item:
        flash("Couldn't find the item with the id of '{}'".format(
            item_id), category='warning')
        return redirect(url_for('url.index'))
    return render_template('detail.html', item=item)


@url.route('/category/<int:category_id>', methods=['GET'])
def category_items(category_id):
    items = Item.query.filter(Item.category_id == category_id).all()
    catergories = Category.query.all()
    if not items:
        flash("Couldn't find any items with this category")
        return redirect(url_for('url.index'))
    return render_template(
        'index.html',
        categories=catergories,
        items=items,
        current_category_id=category_id)


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
            form.name.data.capitalize()), category='success')
        return redirect(url_for('url.index'))
    return render_template('add_category.html', form=form)


@url.route('/add/item', methods=['GET', 'POST'])
@login_required
def add_item():
    form = AddItem()
    if form.validate_on_submit():
        new_item = Item(
            category_id=form.category_id.data.id,
            name=form.name.data.capitalize(),
            description=form.description.data)
        db.session.add(new_item)
        db.session.commit()
        flash("New item '{}' was successfully created".format(
            form.name.data.capitalize()), category='success')
        return redirect(url_for('url.index'))
    return render_template('add_item.html', form=form)
