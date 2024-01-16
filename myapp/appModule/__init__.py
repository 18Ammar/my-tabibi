from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', instance_relative_config=True)

    from .home import home_bp
    app.register_blueprint(home_bp, template_folder='templates', static_folder='static', instance_relative_config=True)

    from .app import app_bp
    app.register_blueprint(app_bp, template_folder='templates', static_folder='static', instance_relative_config=True)

    return app
