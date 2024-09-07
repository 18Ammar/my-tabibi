from flask import Blueprint, render_template, redirect, url_for,abort,flash,request
from flask_login import login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField,  TextAreaField,PasswordField, ValidationError
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, EqualTo, Email
from appModule.appdb import User, db,Post,Follow
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float 
from werkzeug.utils import secure_filename
import os







profile = Blueprint('profile', __name__)



class UpdateProfileForm(FlaskForm):
    username = StringField('Username', render_kw={'placeholder': 'Update your username'})
    email = StringField('Email', render_kw={'placeholder': 'Update your email'})
    password = PasswordField('Password', render_kw={'placeholder': 'Update your password'})
    picPath = FileField("update your picuture",validators=[FileAllowed(["png","jpg","jpeg"])], render_kw={'placeholder': 'update your picuture'})
    about = StringField("about",render_kw={'placeholder': 'about info'})
    def validate_username(self, field):
        if field.data != current_user.username:
            user = User.query.filter_by(username=field.data).first()
            if user:
                raise ValidationError("This username is already taken")

    def validate_email(self, field):
        if field.data != current_user.email:
            user = User.query.filter_by(email=field.data).first()
            if user:
                raise ValidationError("This email is already registered")



class CreateArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Article Content', validators=[DataRequired()])
    image = FileField('Image')
    tag = StringField('Tag', validators=[DataRequired()])



@profile.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    following_number = current_user.following_number()
    follower_number = current_user.follower_number()
    post = Post.query.filter_by(user_id=current_user.id)
    return render_template('profile.html',posts=post, following_number=following_number, follower=follower_number)


@profile.route('/profile/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.home'))

@profile.route('/profile/update', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = UpdateProfileForm()
    if request.method == 'POST':
        username = form.username.data
        email =form.email.data
        password = form.password.data
        about = form.about.data
        if username:
            current_user.username = username
        if email:
            current_user.email = email
        if password:
            bcrypt = Bcrypt()
            pass_hash = bcrypt.generate_password_hash(password).decode("utf-8")
            current_user.password = pass_hash
        if form.picPath.data:
            # print(form.picPath.data)
            pic_file = form.picPath.data
            pic_filename = secure_filename(pic_file.filename)
            pic_path = os.path.join("..//static//images//", pic_filename)
            print(pic_path)
            if os.path.exists(pic_path):
                # print(pic_path)
                # pic_path = pic_path[30:]
                # print(pic_path)
                current_user.image_file = str(pic_path)
                
            else:
                # print(pic_path)
                pic_file.save(pic_path)
                pic_path = pic_path[30:]
                current_user.image_file =str(pic_path)

        if about:
            current_user.about = about
        db.session.commit()  
        return redirect(url_for('profile.user_profile'))
        

    return render_template('update_profile.html', form=form)




@profile.route('/get_profile/<username>', methods=["GET","POST"])
@login_required
def get_profile(username):
    user = User.query.filter_by(username=username).first()
    if user == current_user:
        return redirect(url_for('profile.user_profile'))
    return render_template("viewSelectedProfile.html", user=user)
    



@profile.route('/profile/post/<int:userId>', methods=['GET', 'POST'])
@login_required
def user_post(userId):
    form = CreateArticleForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        tag = form.tag.data
        image = form.image.data
        if image:
            pic_filename = secure_filename(image.filename)
            pic = os.path.join("..//static//images//", pic_filename)
            print(pic)
            if os.path.exists(pic):
                # print(pic_path)
                # pic_path = pic_path[30:]
                # print(pic_path)
                post.post_image = str(pic)

                
            else:
                # print(pic_path)
                image.save(pic)
                pic_ = pic[30:]
                post.post_image = str(pic)

    
        new_post = Post(title=title, content=content,tag=tag,author=current_user,image=image)
        db.session.add(new_post)
        db.session.commit()
    posts = Post.query.filter_by(user_id=int(userId)).all()
    if posts:
        return render_template('user_post.html',userId=userId, form=form,posts=posts)
    else:
        return render_template('user_post.html',userId=userId, form=form,posts=None)


@profile.route('/profile/post/update/<post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CreateArticleForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.tag = form.tag.data
        
        image = form.image.data
        if image:
            pic_filename = secure_filename(image.filename)
            pic = os.path.join("..//static//images//", pic_filename)
            print(pic)
            if os.path.exists(pic):
                # print(pic_path)
                # pic_path = pic_path[30:]
                # print(pic_path)
                post.post_image = str(pic)

                
            else:
                # print(pic_path)
                image.save(pic)
                pic_ = pic[30:]
                post.post_image = str(pic)


        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for("profile.user_post",userId=post.author.id))

    return render_template("update_post.html", form=form, post=post)




@profile.route('/profile/post/delete/<post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=int(post_id)).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("profile.user_profile"))



@profile.route("/profile/follow/<user_id>",methods=["POST","GET"])
@login_required
def add_follow(user_id):
    print(user_id)
    new_follow = Follow(following_id=current_user.id,follower_id=user_id)
    db.session.add(new_follow)
    db.session.commit()
    return "new follow"


