from flask import Blueprint, abort
from flask.json import jsonify
from sqlalchemy.orm import lazyload

# from catalog import db
from catalog.models import Category, Item

json_url = Blueprint('json_url', __name__)


@json_url.route('/json/all', methods=['GET'])
def json_all():
    categories = Category.query.options(lazyload('items')).all()
    if not categories:
        return abort(404)
    category_list = []
    for category in categories:
        item_list = []
        for item in category.items:
            item_list.append(item.serialize)
        serialized_category = category.serialize
        serialized_category['items'] = item_list
        category_list.append(serialized_category)
    return jsonify(category_list)


@json_url.route('/json/categories', methods=['GET'])
def json_categories():
    categories = Category.query.all()
    if not categories:
        return abort(404)
    return jsonify([category.serialize for category in categories])


@json_url.route('/json/items', methods=['GET'])
def json_items():
    items = Item.query.all()
    if not items:
        return abort(404)
    return jsonify([item.serialize for item in items])


@json_url.route('/json/category/<int:category_id>', methods=['GET'])
def json_category(category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify(category.serialize)


@json_url.route('/json/item/<int:item_id>', methods=['GET'])
def json_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.serialize)
