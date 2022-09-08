from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY']='807fdbc9826fa98b86b8feb314d9f0fb'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'


from app import route
