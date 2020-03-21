import firebase_admin

from flask import Flask, flash, render_template
from flask_login import LoginManager
from models.models import db as db
from views.home import home as home_view
from views.seo import seo as seo_view
from models.models import UserInfo

# Enables Instance Folder Configuration (instance_relative_config=True) 
app = Flask(__name__, instance_relative_config=True)

# Configuration Files From Instance Folder
app.config.from_pyfile('app_config.py')
app.config.from_pyfile('firebase_config.py')
app.config.from_pyfile('models_config.py')

# Enable instance of SQLAlchemy
db.init_app(app)

# Enable Firebase Admin
fba = firebase_admin.initialize_app()

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

# Home
app.register_blueprint(home_view)

# Search Engine Optimization - SEO
app.register_blueprint(seo_view)

# Register the Service Worker
@app.route('/sw.js', methods=['GET'])
def serviceworker():
    return app.send_static_file('js/sw.js')

# @app.route('/user/<username>/')
# def user(username):
#     return 'This is a second URL Test for variables on URL. Your username is: %s' % username