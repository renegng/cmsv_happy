import firebase_admin

from firebase_admin import auth, credentials
from flask import flash, render_template
from flask import current_app as app
from flask_login import LoginManager
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
        return UserInfo.query.filter(UserInfo.uid == uid).first()
    return None

@lim.unauthorized_handler
def unauthorized():
    flash('Debes Iniciar sesión o Registrarte para ingresar.', 'error')
    return redirect(url_for('home_view._welcome'))