from . import auth, db
from datetime import datetime
from flask import Blueprint, redirect, render_template, request, url_for, jsonify
from flask import current_app as app
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

        # Query the user in the DB.
        user = UserInfo.query.filter_by(uid = uid).first()
        if user is None:
            # User is not registered on DB. Insert user, create session and redirect to next step
            user = UserInfo()
            user.uid = uid
            user.email = decoded_token['email']
            user.name = decoded_token['name']
            user.datecreated = datetime.utcnow()
            user.cmsvuserid = 'CMSV-' + user.name.strip().upper()[0:1] + user.datecreated.strftime('-%y%m%d-%H%M%S')
            
            db.session.add(user)
            db.session.commit()
            app.logger.info('** SWING_CMS ** - LoginUser added: {}'.format(user.id))
            
        return jsonify({ 'status': 'success' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - LoginUser Error: {}'.format(e))
        return jsonify({ 'status': 'error' })

@home.route('/home/')
def _home():
    app.logger.debug('** SWING_CMS ** - Home accessed')
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