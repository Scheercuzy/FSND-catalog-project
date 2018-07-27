from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, current_user

from catalog.forms import CategoryForm, ItemForm
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
        flash("Couldn't find any items with this category", category='warning')
    return render_template(
        'index.html',
        categories=catergories,
        items=items,
        current_category_id=category_id)


@url.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('url.index'))
    return render_template('login.html')


@url.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Successfully signed out", category='info')
    return redirect(url_for('url.index'))


@url.route('/add/category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        new_category = Category(name=form.name.data.capitalize())
        db.session.add(new_category)
        db.session.commit()
        flash("Successfully created new category '{}'".format(
            form.name.data.capitalize()), category='success')
        return redirect(url_for('url.index'))
    return render_template(
        'forms/form.html',
        form_title="Add Category",
        form=form,
        form_name='category',
        action=url_for('url.add_category')
    )


@url.route('/delete/category/<int:category_id>', methods=['GET'])
@login_required
def delete_category(category_id):
    category = Category.query.filter(Category.id == category_id).first()
    if not category:
        flash("Couldn't find a category with that id", category='warning')
        return redirect(request.referrer)

    items = Item.query.filter(Item.category_id == category_id).all()
    if items:
        flash(
            "Couldn't remove category because of items {}. "
            "Remove those items first before deleting this category".format(
                ", ".join([item.name for item in items])),
            category='warning')
        return redirect(request.referrer)

    category_name = category.name
    db.session.delete(category)
    db.session.commit()
    flash(
        "Successfuly deleted category '{}'".format(category_name),
        "success")

    return redirect(url_for('url.index'))


@url.route('/edit/category/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    category = Category.query.filter(Category.id == category_id).first()
    if not category:
        flash("Couldn't find a category with that id", category='warning')
        return redirect(request.referrer)

    form = CategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Successfully updated category', 'success')
        return redirect(url_for('url.index'))

    elif request.method == 'GET':
        form.name.data = category.name

    return render_template(
        'forms/form.html',
        form_title='Edit Category',
        form=form,
        form_name='category',
        action=url_for('url.edit_category', category_id=category_id))


@url.route('/add/item', methods=['GET', 'POST'])
@login_required
def add_item():
    form = ItemForm()
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
    return render_template(
        'forms/form.html',
        form_title='Add Item',
        form=form,
        form_name='item',
        action=url_for('url.add_item'))


@url.route('/delete/item/<int:item_id>', methods=['GET'])
@login_required
def delete_item(item_id):
    item = Item.query.filter(Item.id == item_id).first()
    if not item:
        flash("Couldn't find an item with that id", category='warning')
        return redirect(request.referrer)

    item_name = item.name
    db.session.delete(item)
    db.session.commit()
    flash(
        "Successfuly deleted item '{}'".format(item_name),
        "success")

    return redirect(url_for('url.index'))


@url.route('/edit/item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Item.query.filter(Item.id == item_id).first()
    if not item:
        flash("Couldn't find a item with that id", category='warning')
        return redirect(request.referrer)

    form = ItemForm()
    if form.validate_on_submit():
        item.category_id = form.category_id.data.id
        item.name = form.name.data
        item.description = form.description.data
        db.session.commit()
        flash('Successfully updated Item', 'success')
        return redirect(url_for('url.index'))

    elif request.method == 'GET':
        form.name.data = item.name
        form.description.data = item.description

    return render_template(
        'forms/form.html',
        form_title='Edit Item',
        form=form,
        form_name='item',
        action=url_for('url.edit_item', item_id=item_id))
