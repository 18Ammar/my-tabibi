from flask import Blueprint, flash, render_template, redirect, url_for, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_sqlalchemy import SQLAlchemy
from appModule.appdb import User,db
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail, Message

sign_in_bp = Blueprint('sign_in', __name__)

mail = Mail()

class SignInForm(FlaskForm):
    username = StringField(render_kw={'placeholder': 'Username'}, validators=[DataRequired()])
    password = PasswordField(render_kw={'placeholder': 'Password'}, validators=[DataRequired()])

class RequestResetPasswordForm(FlaskForm):
    email = StringField(render_kw={'placeholder': 'Email'}, validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email")

class ResetPasswordForm(FlaskForm):
    password = PasswordField(render_kw={'placeholder': 'New Password'}, validators=[DataRequired()])
    confirm_password = PasswordField(render_kw={'placeholder': 'Confirm Password'}, validators=[DataRequired()])
    submit = SubmitField('Reset Password')

@sign_in_bp.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect('profile')

    form = SignInForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        bcrypt = Bcrypt()
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash("There is no account with that username or email", "error")
            return render_template('sign_in.html', form=form)

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect("profile")
        else:
            flash("Invalid username or password", "error")
   
    return render_template('sign_in.html', form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    
    msg = Message("Password reset request",
                  sender="amar2003895@fastmail.com",
                  recipients=[user.email])
    
    msg.body = f"""To reset your password, visit the following link:
{url_for('sign_in.reset_token', token=token, _external=True)}"""
    
    mail.send(msg)

@sign_in_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect('profile')
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash("An email has been sent to your account to reset your password.","warning")
        else:
            flash("There is no account with this email", "error")
        
    return render_template('reset_request.html', form=form)

@sign_in_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect('profile')
    user = User.verify_token(token)
    if user is None:
        flash("Invalid or expired token", "error")
        return redirect(url_for('sign_in.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        bcrypt = Bcrypt()
        pass_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        user.password = pass_hash
        db.session.commit()
        return redirect(url_for("sign_in.sign_in"))
    return render_template('reset_password.html', form=form,token=token)
