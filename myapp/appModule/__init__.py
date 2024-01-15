from flask import Flask
app = Flask(__name__,template_folder='myapp/templates',static_folder='myapp/static',instance_relative_config=True)  



def create_app():
    app = Flask(__name__)

    from .home import home_bp
    app.register_blueprint(home_bp)
    from .app import app_bp
    app.register_blueprint(app_bp)
   

    return app
