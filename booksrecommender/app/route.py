from flask import render_template,url_for,flash,redirect,request
from app import app,db
from app.recommender import runRecommender
from app.forms import RegistrationForm,LoginForm,updateEmail,RatingForm
from flask_login import login_user,current_user,logout_user,login_required
from app.models import User,Rating
from sqlalchemy import create_engine
import json
import os



@app.route('/')
@app.route('/index',methods=['GET'])
def index():

    return render_template('index.html',title="BookRecommendation System")

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        max_id = db.session.query(db.func.max(User.user_id)).scalar()
        user=User(user_id=max_id+1,email=form.email.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.email.data}!Please login','success')
        return redirect(url_for('index'))
    return render_template('register.html',title='Register',form=form)
@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:    
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and str(form.password.data)==user.password:
            login_user(user,remember=form.remember.data)

            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful','danger')

    return render_template('login.html',title='Login',form=form)

@app.route('/home')
@login_required
def home():
    return render_template('home.html', title='Home')

@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    print("User:::::",current_user.user_id)
    form=updateEmail()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
        elif request.method == 'GET':
            form.email.data = current_user.email
        return render_template('account.html', title='Account',
                            form=form)
    else:
        available=False
        fileRating = os.path.join(app.static_folder, 'ratings.json')
        fileBook=os.path.join(app.static_folder, 'books.json')
        
        with open(fileRating) as f:
                dataRating = json.load(f)
        for i in range(len(dataRating)):
            if dataRating[i]["user_id"]==current_user.user_id:
                print(dataRating[i]["user_id"])
                available=True
        if available==False:
            suggested=[{"book_id":0,"original_title":"No rating, data unavailable","genre":"-"}]
            rated=[{"book_id":0,"original_title":"No rating, data unavailable","genre":"-"}]
        if available==True:
            predict,rated=runRecommender(fileBook,fileRating,current_user.user_id)
            suggested=json.loads(predict)
            rated=json.loads(rated)
        return render_template('account.html', title='Account',form=form,suggested=suggested,rated=rated)

    return render_template('account.html', title='Account',form=form)

@app.route('/recommend',methods=['GET','POST'])
@login_required
def recommend():
    book=""
    rating=""
    form=RatingForm()

    if request.method == 'POST':
        print(form.book_id.data)
        if form.validate_on_submit():
            redundant=False
            filename = os.path.join(app.static_folder, 'ratings.json')

            jsonData={"user_id":current_user.user_id,"book_id":form.book_id.data,"rating":form.rating.data}
            with open(filename) as f:
                data = json.load(f)
            for i in range(len(data)):
                if data[i]["user_id"]==current_user.user_id and data[i]["book_id"]==form.book_id.data:
                    redundant=True
            if redundant==False:
                data.append(jsonData)

                with open(filename, 'w') as f:
                    json.dump(data, f)
                    flash('Your rating has been updated!', 'success')
            else:
                flash('Rating unsuccessful, you have rated the movie','danger')
            return redirect(url_for('recommend'))
        else:
            flash('Rating Unsuccessful','danger')
    return render_template('recommend.html',book=book,form=form, title='Recommend')


@app.route('/book',methods=['GET','POST'])
@login_required
def book():
    if request.method == 'GET':
        with open('/test code/booksrecommendation/booksrecommender/app/static/books.json', 'r', encoding="utf8") as blog_file:
            book = json.load(blog_file)
    return render_template('book.html',book=book, title='Book')
@app.route('/about')
@login_required
def about():
    return render_template('about.html',title='About')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



