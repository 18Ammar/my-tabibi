from flask import Blueprint, render_template,flash,jsonify
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo,Length

sign_up_bp = Blueprint('sign_up', __name__)

class SignUp(FlaskForm):
    email = EmailField(render_kw={"placeholder": "Enter your email"},validators=[DataRequired()])
    password = PasswordField(render_kw={"placeholder": "Enter your password"},validators=[DataRequired(),Length(min=8),EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField(render_kw={"placeholder": "Confirm your password"},validators=[DataRequired(),Length(min=8),EqualTo('password', message='Passwords must match')])


@sign_up_bp.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    form = SignUp()
    
    if form.validate_on_submit():
        password = form.password.data
        email = form.email.data
        print(jsonify({'email': email, 'password': password}))
        return jsonify({'email': email, 'password': password})
    
    return render_template('sign_up.html', form=form)