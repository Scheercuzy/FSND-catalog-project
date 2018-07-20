from flask import Blueprint

url = Blueprint('url', __name__)


@url.route('/')
@url.route('/hello')
def HelloWorld():
    return "Hello World"
