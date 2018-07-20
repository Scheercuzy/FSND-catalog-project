from flask import Flask
from catalog.routes import url

app = Flask(__name__)
app.register_blueprint(url)
