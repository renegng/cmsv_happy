from flask import Blueprint, redirect, render_template, request, url_for

home = Blueprint('home', __name__, template_folder='templates', static_folder='static')

@home.route('/')
def _index():
    return redirect(url_for('home._welcome'))

@home.route('/welcome/')
def _welcome():
    return render_template('welcome.html')

@home.route('/loginUser/', methods=['POST'])
def _loginUser():
    print('LLEGAMOS A LOGIN USER!')
    print(request.json['idToken'])
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