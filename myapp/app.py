from flask import Flask
import os

app = Flask(__name__)
config_file_path = 'd:\\health_AI\\instance\\config.py' 
app.config.from_pyfile(config_file_path)
app.secret_key = app.config.get('SECRT_KEY','')

from appModule.home import home_bp
app.register_blueprint(home_bp)

from appModule.app import app_bp
app.register_blueprint(app_bp)

from appModule.sign_in import sign_in_bp
app.register_blueprint(sign_in_bp)

from appModule.sign_up import sign_up_bp
app.register_blueprint(sign_up_bp)

from appModule.chat_ai import chat_ai
app.register_blueprint(chat_ai)

if __name__ == '__main__':
    app.run(debug=True)
