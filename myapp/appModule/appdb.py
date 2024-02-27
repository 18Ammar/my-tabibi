from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from appModule.config import SECRET_KEY

db = SQLAlchemy()

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='default.png')
    about = db.Column(db.String(200), nullable=True)
    posts = db.relationship('Post', backref='author', lazy="joined")
    
    
    followers = db.relationship("Follow", backref="follower", foreign_keys='[Follow.follower_id]')
    following = db.relationship("Follow", backref="following", foreign_keys='[Follow.following_id]')
    message_sent = db.relationship("Message",backref="sender",foreign_keys='Message.sender_id')
    message_recived = db.relationship("Message",backref="receiver",foreign_keys="Message.receiver_id")

    def follower_number(self):
        return len(self.followers)

    def following_number(self):
        return len(self.following)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(SECRET_KEY, expires_in=expires_sec) 
        return s.dumps({"user_id": self.id}).decode("utf-8")
        
    @staticmethod
    def verify_token(token):
        s = Serializer(SECRET_KEY)
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tag = db.Column(db.String(100), nullable=True)
    post_image = db.Column(db.String(120), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=db.func.now())
    like = db.relationship("Like",backref="like",lazy=True)
    comment = db.relationship("Comment",backref="comment",lazy=True)



class Follow(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    following_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    follower_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)



class Like(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey("post.id"),nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey("post.id"),nullable=False)
    date_post = db.Column(db.DateTime,nullable=False,default=db.func.now())




class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id")) 
    contact_id = db.Column(db.Integer, db.ForeignKey("user.id")) 
    user = db.relationship("User", foreign_keys=[user_id], backref="contacts")
    contact = db.relationship("User", foreign_keys=[contact_id])


class Message(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    sender_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    receiver_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    content = db.Column(db.Text,nullable=False)
    date_sent = db.Column(db.DateTime,nullable=False,default=db.func.now())
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False)
    room = db.relationship("Room", backref="messages")

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)