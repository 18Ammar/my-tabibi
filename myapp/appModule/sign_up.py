from flask import Blueprint, render_template,flash,jsonify,redirect
from flask_wtf import FlaskForm
from wtforms import ValidationError,EmailField, PasswordField,StringField
from wtforms.validators import DataRequired, EqualTo,Length
from flask_sqlalchemy import SQLAlchemy
from appModule.appdb import User,db
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,UserMixin,current_user




sign_up_bp = Blueprint('sign_up', __name__)
LoginManager = LoginManager()

@LoginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class SignUp(FlaskForm):
    username = StringField(render_kw={'placeholder': 'username'},validators=[DataRequired()])
    email = EmailField(render_kw={"placeholder": "Enter your email"},validators=[DataRequired()])
    password = PasswordField(render_kw={"placeholder": "Enter your password"},validators=[DataRequired(),Length(min=8),EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField(render_kw={"placeholder": "Confirm your password"},validators=[DataRequired(),Length(min=8),EqualTo('password', message='Passwords must match')])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is already taken")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is already registered")

@sign_up_bp.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if current_user.is_authenticated:
        return redirect('profile')
    form = SignUp()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        bcrypt = Bcrypt()
        pass_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(username=username,email=form.email.data, password=pass_hash)
        db.session.add(user)
        db.session.commit()
        return redirect("sign-in")
    
    
    return render_template('sign_up.html', form=form)