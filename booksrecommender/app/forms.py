from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError,NumberRange
from flask_login import current_user

from app.models import User
class RegistrationForm(FlaskForm):
    email= StringField('Email:',validators=[DataRequired(),Email()])
    password = PasswordField('Password:',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password:',validators=[DataRequired(),EqualTo('password')])

    submit=SubmitField('Sign Up')
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken')
class LoginForm(FlaskForm):
    email= StringField('Email:',validators=[DataRequired(),Email()])
    password = PasswordField('Password:',validators=[DataRequired()])
    remember=BooleanField('Remember Me:')

    submit=SubmitField('Login')

class updateEmail(FlaskForm):
    email= StringField('Email:',validators=[DataRequired(),Email()])
    submit=SubmitField('Update')

    def validate_email(self,email):
        if email.data!= current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken')
class RatingForm(FlaskForm):
    book_id= IntegerField('Book ID:',validators=[DataRequired(),NumberRange(min=1, max=9999)])

    rating = IntegerField('Rating:',validators=[DataRequired(),NumberRange(min=0, max=5)])
    def validateRating(self,rating):
        if rating.data>5 and rating.data<0:
            raise ValidationError('Invalid rating')

    submit=SubmitField('Submit')
