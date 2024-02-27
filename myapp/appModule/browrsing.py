from flask import Blueprint, render_template
from flask_login import login_required
from appModule.appdb import User,Post
browse = Blueprint('browser',__name__)

@browse.route('/browse',methods=['get', 'post'])
@login_required
def show_content():
    posts = Post.query.all()
    return render_template('browsing.html',posts=posts)

@browse.route('/browse/artical/<int:post_id>',methods=['get', 'post'])
@login_required
def show_artical(post_id):
    print(post_id)
    post = Post.query.filter_by(id=int(post_id)).first()
    return render_template('view_artical.html',post=post)