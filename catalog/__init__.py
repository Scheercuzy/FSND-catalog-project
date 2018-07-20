from flask import Flask
from catalog.routes import url
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.register_blueprint(url)
app.config['SECRET_KEY'] = '6eL0O65HUS3RMcAQTFuz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
