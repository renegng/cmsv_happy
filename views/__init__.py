import datetime
import firebase_admin

from firebase_admin import auth, credentials
from flask import flash, render_template, jsonify
from flask import current_app as app
from flask_login import LoginManager, login_user, current_user, logout_user
from models.models import db
from models.models import UserInfo

# Enable instance of SQLAlchemy
db.init_app(app)

# Enable Firebase Admin
cred = credentials.Certificate(app.config.get('GOOGLE_APPLICATION_CREDENTIALS'))
fba = firebase_admin.initialize_app(cred)

# Enable Flask-Login
lim = LoginManager()
lim.init_app(app)
lim.login_view = 'home_view._welcome'

@lim.user_loader
def load_user(uid):
    if uid is not None:
        return UserInfo.query.filter_by(uid = uid).first()
    return None

@lim.unauthorized_handler
def unauthorized():
    flash('Debes Iniciar sesión o Registrarte para ingresar.', 'error')
    return redirect(url_for('home_view._welcome'))

# Creates a Flask-Login Session instance
def createLoginSession(user):
    try:
        user.is_active = user.enabled
        user.is_authenticated = True
        return login_user(user)
    except Exception as e:
        app.logger.error('** SWING_CMS ** - CreateLoginSession Error: {}'.format(e))
        return jsonify({ 'status': 'error' })

# Creates a Firebase Cookie Session instance
def createCookieSession(idToken, cmd = None, action = None):
    try:
        # Set session expiration to 14 days.
        expires_in = datetime.timedelta(days = 14)

        # Set cookie policy for session cookie.
        expires = datetime.datetime.now() + expires_in

        # Create the session cookie. This will also verify the ID token in the process.
        # The session cookie will have the same claims as the ID token.
        session_cookie = auth.create_session_cookie(idToken, expires_in = expires_in)

        # Create an HTTP Response with a JSON Success Status and attach the cookie to it.
        jsonData = {
            'status': 'success',
            'cmd': cmd,
            'action': action
        }
        response = jsonify(jsonData)

        if app.config['ENV'] == 'development':
            # Cookies for Development
            response.set_cookie('cmsv-happy-session', session_cookie, expires = expires, httponly = True)
        else:
            # Cookies for Production
            response.set_cookie('cmsv-happy-session', session_cookie, expires = expires, httponly = True, samesite = 'Lax', secure = True)

        return response
    except Exception as e:
        app.logger.error('** SWING_CMS ** - CreateCookieSession Error: {}'.format(e))
        return jsonify({ 'status': 'error' })