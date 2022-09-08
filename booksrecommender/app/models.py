from app import db,login_manager
from flask_login import UserMixin
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model,UserMixin):
    user_id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(30),unique=True,nullable=False)
    password=db.Column(db.Integer,nullable=False)
    def get_id(self):
           return (self.user_id)
    def __repr__(self):
        return f"User('{self.email}','{self.password}')"

class Rating(db.Model):
    user_id=db.Column(db.Integer,primary_key=True)
    book_id=db.Column(db.Integer)
    rating=db.Column(db.Integer)

    def __repr__(self):
        return f"Rating('{self.user_id}','{self.rating}','{self.user_id}')"

class Books(db.Model):
    book_id=db.Column(db.Integer,primary_key=True)
    genre=db.Column(db.String(100))

    def __repr__(self):
        return f"Books('{self.book_id}','{self.genre}')"
    
