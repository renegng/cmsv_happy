from flask import Flask

# Enables Instance Folder Configuration (instance_relative_config=True) 
app = Flask(__name__, instance_relative_config=True)

# Configuration Files From Instance Folder
app.config.from_pyfile('config_app.py')
app.config.from_pyfile('config_firebase.py')
app.config.from_pyfile('config_models.py')

with app.app_context():
    from views.home import home as home_view
    from views.seo import seo as seo_view

    # Home
    app.register_blueprint(home_view)

    # Search Engine Optimization - SEO
    app.register_blueprint(seo_view)

    # Register the Service Worker
    @app.route('/sw.js', methods=['GET'])
    def serviceworker():
        return app.send_static_file('js/sw.js')

