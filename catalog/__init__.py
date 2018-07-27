from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.config['SECRET_KEY'] = '6eL0O65HUS3RMcAQTFuz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
login_manager.login_view = 'url.login'
login_manager.login_message_category = "warning"

from catalog.routes import url  # noqa
from catalog.oauth import google_blueprint  # noqa
from catalog.models import OAuth, User  # noqa


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(google_blueprint, url_prefix="/login")
app.register_blueprint(url)


db.init_app(app)
login_manager.init_app(app)
csrf.init_app(app)
