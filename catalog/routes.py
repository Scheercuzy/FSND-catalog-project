from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, logout_user

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
