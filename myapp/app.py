from flask import Flask
from appModule.appdb import db
from appModule.sign_up import LoginManager
from appModule.sign_in import mail
from appModule.chat_ai import socket
import os


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

app = Flask(__name__)


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
app.secret_key = "thisisSECRETKEY"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///mydb.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  
app.config["MAIL_SERVER"]= "smtp.fastmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "amar2003895@fastmail.com"
app.config["MAIL_PASSWORD"] = "7w3eezbuntdudum7"


socket.init_app(app)
mail.init_app(app)
LoginManager.init_app(app)
db.init_app(app)


from appModule.home import home_bp
app.register_blueprint(home_bp)

from appModule.sign_in import sign_in_bp
app.register_blueprint(sign_in_bp)

from appModule.sign_up import sign_up_bp
app.register_blueprint(sign_up_bp)

from appModule.chat_ai import chat_ai
app.register_blueprint(chat_ai)

from appModule.browrsing import browse
app.register_blueprint(browse)

from appModule.image_scanner import img_scan
app.register_blueprint(img_scan)

from appModule.user_profile import profile
app.register_blueprint(profile)

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    socket.run(app=app,debug=False) 