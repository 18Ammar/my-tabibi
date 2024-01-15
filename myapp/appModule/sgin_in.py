from flask import Blueprint, render_template

sign_in_bp = Blueprint('sign_in', __name__)

@sign_in_bp.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')
