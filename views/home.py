from flask import Blueprint, render_template

home = Blueprint('home', __name__, template_folder='templates', static_folder='static')

@home.route('/')
def _landing_page():
    return render_template('landing_page.html')

@home.route('/acercade/')
def _acercade():
    return render_template('acercade.html')

@home.route('/politicaprivacidad/')
def _politicaprivacidad():
    return render_template('politicaprivacidad.html')

@home.route('/terminosdelservicio/')
def _terminosdelservicio():
    return render_template('terminosdelservicio.html')