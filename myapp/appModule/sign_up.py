from flask import Blueprint, render_template

sign_up_bp = Blueprint('sign_up', __name__)

@sign_up_bp.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')
