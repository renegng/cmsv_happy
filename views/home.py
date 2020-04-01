import datetime

from . import auth, db, createLoginSession, createCookieSession
from flask import Blueprint, redirect, render_template, request, url_for, jsonify
from flask import current_app as app
from flask_login import logout_user
from models.models import UserInfo, UserRole, UserXRole

home = Blueprint('home', __name__, template_folder='templates', static_folder='static')

@home.route('/')
def _index():
    return redirect(url_for('home._welcome'))

@home.route('/welcome/')
def _welcome():
    return render_template('welcome.html')

@home.route('/loginUser/', methods=['POST'])
def _loginUser():
    try:
        # Retrieve the uid from the JWT idToken
        idToken = request.json['idToken']
        decoded_token = auth.verify_id_token(idToken)
        uid = decoded_token['uid']

        # Search for the user in the DB.
        user = UserInfo.query.filter_by(uid = uid).first()
        if user is None:
            # Retrieve Firebase's User info
            fbUser = auth.get_user(uid)

            # User is not registered on DB. Insert user in DB.
            user = UserInfo()
            user.uid = uid
            user.email = fbUser.email
            user.name = fbUser.display_name
            user.datecreated = datetime.datetime.utcnow()
            user.cmsvuserid = 'CMSV-' + user.name.strip().upper()[0:1] + user.datecreated.strftime('-%y%m%d-%H%M%S')
            
            db.session.add(user)
            db.session.commit()
            app.logger.info('** SWING_CMS ** - LoginUser added: {}'.format(user.id))
        
        # Create User Session
        createLoginSession(user)
        
        # Return Session Cookie
        response = createCookieSession(idToken, True, '/terminosdelservicio/')
        return response

    except Exception as e:
        app.logger.error('** SWING_CMS ** - LoginUser Error: {}'.format(e))
        return jsonify({ 'status': 'error' })

@home.route('/home/')
def _home():
    app.logger.debug('** SWING_CMS ** - Home accessed')
    logout_user()
    return render_template('acercade.html')

@home.route('/acercade/')
def _acercade():
    return render_template('acercade.html')

@home.route('/politicaprivacidad/')
def _politicaprivacidad():
    return render_template('politicaprivacidad.html')

@home.route('/terminosdelservicio/')
def _terminosdelservicio():
    return render_template('terminosdelservicio.html')