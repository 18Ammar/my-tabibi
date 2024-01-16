from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
sign_in_bp = Blueprint('sign_in', __name__)

class SignInForm(FlaskForm):
    username = StringField(render_kw={'placeholder': 'Username'},validators=[DataRequired()])
    password = PasswordField(render_kw={'placeholder': 'Password'},validators=[DataRequired()])

@sign_in_bp.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    username = form.username.data
    password = form.password.data
    print(username, password)
    return render_template('sign_in.html', form=form)
