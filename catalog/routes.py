from flask import Blueprint, render_template

url = Blueprint('url', __name__)


@url.route('/')
def index():
    return render_template('index.html', title="index")
