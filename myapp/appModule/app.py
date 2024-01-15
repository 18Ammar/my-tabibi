from flask import Blueprint, render_template

app_bp = Blueprint('app', __name__)

@app_bp.route('/')
def index():
    return render_template('homepage.html')
