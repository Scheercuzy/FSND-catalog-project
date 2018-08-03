from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, current_user

from catalog.forms import CategoryForm, ItemForm
from catalog import db
from catalog.models import Category, Item

url = Blueprint('url', __name__)


@url.route('/')
def index():
    """ Index page for the application. Loads all the categories and items
    for the current user or if the user isn't signed in, flashes a message
    to do so"""

    if current_user.is_anonymous:
        flash("Login to add, edit and delete items", category='warning')
        return render_template('index.html', title="index")
    else:
        categories = Category.query.filter(
            current_user.id == Category.user_id).all()
        items = Item.query.filter(current_user.id == Item.user_id).all()
    return render_template(
        'index.html',
        title="index",
        categories=categories,
        items=items,
        category_id=None)


@url.route('/item/<int:item_id>', methods=['GET'])
@login_required
def item_detail(item_id):
    """Item detail page of the application. If the item isn't found
    the user is redirected to the index page with a flash message
    saying the item wasn't found"""

    item = Item.query.filter(
        Item.id == item_id,
        current_user.id == Item.user_id
    ).first()
    if not item:
        flash("Couldn't find this item", category='warning')
        return redirect(url_for('url.index'))
    return render_template('detail.html', item=item)


@url.route('/category/<int:category_id>', methods=['GET'])
@login_required
def category_items(category_id):
    """When a Category is selected, all items in a relationship
    with it are shown on the page. This checks if it exists and
    which items are linked to the specific category selected"""

    items = Item.query.filter(
        Item.category_id == category_id,
        Item.user_id == current_user.id
    ).all()
    categories = Category.query.filter(
        Category.user_id == current_user.id).all()
    if not categories:
        flash("Couldn't find this category", category='warning')

    return render_template(
        'index.html',
        categories=categories,
        items=items,
        current_category_id=category_id)


@url.route('/login')
def login():
    """A simple login page with all the available OAuth providers """

    if current_user.is_authenticated:
        return redirect(url_for('url.index'))
    return render_template('login.html')


@url.route('/logout')
@login_required
def logout():
    """Logout out the user"""
    logout_user()
    flash("Successfully signed out", category='info')
    return redirect(url_for('url.index'))


@url.route('/add/category', methods=['GET', 'POST'])
@login_required
def add_category():
    """This is to add a new category. Checks if the user already created a
    category with the same name. Also adds the data to the database once the
    user submitted the form"""

    form = CategoryForm()
    form.name.current_user_id = current_user.id

    if form.validate_on_submit():
        new_category = Category(
            name=form.name.data.capitalize(), user_id=current_user.id)
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
    """Checks if the category id and user exists in the database.
    If it does the category is deleted with all the items related to it"""

    category = Category.query.filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()

    if not category:
        flash("Couldn't find that category", category='warning')
        return redirect(request.referrer)

    category_name = category.name
    db.session.delete(category)
    db.session.commit()
    flash(
        "Successfully deleted category '{}'".format(category_name),
        "success")

    return redirect(url_for('url.index'))


@url.route('/edit/category/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    """Searches the database for the category_id and user_id of the current
    user to find the category name. if it exists a form with its information
    is shown. Once submitted, the data is validated and updated on the database
    """

    category = Category.query.filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()

    if not category:
        flash("Couldn't find that category", category='warning')
        return redirect(request.referrer)

    form = CategoryForm()
    form.name.current_user_id = current_user.id

    if form.validate_on_submit():
        category.name = form.name.data.capitalize()
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
    """This is to add a new item. Once submitted, it checks is the pair of
    category_id and name already exists in the database. Then if it doesn't
    the data is added to the database"""

    form = ItemForm()
    # Query for select field
    form.category_id.query = Category.query.filter(
        Category.user_id == current_user.id).all()

    if form.validate_on_submit():
        new_item = Item(
            category_id=form.category_id.data.id,
            name=form.name.data.capitalize(),
            description=form.description.data,
            user_id=current_user.id)
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
    """Checks if the item with the same id and linked to the same user exists. If
    it does the item is deleted from the database"""

    item = Item.query.filter(
        Item.id == item_id,
        Item.user_id == current_user.id
    ).first()

    if not item:
        flash("Couldn't find the item", category='warning')
        return redirect(request.referrer)

    item_name = item.name
    db.session.delete(item)
    db.session.commit()
    flash(
        "Successfully deleted item '{}'".format(item_name),
        "success")

    return redirect(url_for('url.index'))


@url.route('/edit/item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    """Searches the database for the user_id and item_id key pair, if found a form
    with the data found in the database is added to the form and given to the
    user. Once submitted, Checks if the name already exists with the same
    category_id and different item_id then adds it to the database"""

    item = Item.query.filter(
        Item.id == item_id,
        Item.user_id == current_user.id
    ).first()

    if not item:
        flash("Couldn't find a item with that id", category='warning')
        return redirect(request.referrer)

    form = ItemForm()
    form.editting_item_id = item_id
    # Query for select field
    form.category_id.query = Category.query.filter(
        Category.user_id == current_user.id).all()

    if form.validate_on_submit():
        item.category_id = form.category_id.data.id
        item.name = form.name.data.capitalize()
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
