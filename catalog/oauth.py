from flask import flash
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer import oauth_authorized, oauth_error
from sqlalchemy.orm.exc import NoResultFound
from flask_login import login_user, current_user
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend

from catalog.models import User, OAuth
from catalog import db

google_blueprint = make_google_blueprint(
    client_id="439962279189-oqka6r921tq6p7mq2l3ujj65hbnvqmqg"
    ".apps.googleusercontent.com",
    client_secret="VFUyyM2x_8zvf3UeK0HoUle8",
    scope=["https://www.googleapis.com/auth/userinfo.email",
           "https://www.googleapis.com/auth/userinfo.profile"]
)


google_blueprint.backend = SQLAlchemyBackend(
    OAuth, db.session, user=current_user)


# create/login local user on successful OAuth login
@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with Google.", category="danger")
        return False

    resp = blueprint.session.get("/oauth2/v2/userinfo")
    if not resp.ok:
        msg = "Failed to fetch user info from Google."
        flash(msg, category="danger")
        return False

    google_info = resp.json()
    google_user_id = str(google_info["id"])

    query = OAuth.query.filter_by(
        provider=blueprint.name,
        provider_user_id=google_user_id,
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=google_user_id,
            token=token,
        )

    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in with Google.", category='success')

    else:
        user = User(
            email=google_info["email"],
            name=google_info["name"],
            avatar=google_info["picture"]
        )
        oauth.user = user
        db.session.add_all([user, oauth])
        db.session.commit()
        login_user(user)
        flash("Successfully signed in with Google.", category='success')

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False


# notify on OAuth provider error
@oauth_error.connect_via(google_blueprint)
def google_error(blueprint, error, error_description=None, error_uri=None):
    msg = (
        "OAuth error from {name}! "
        "error={error} description={description} uri={uri}"
    ).format(
        name=blueprint.name,
        error=error,
        description=error_description,
        uri=error_uri,
    )
    flash(msg, category="danger")
