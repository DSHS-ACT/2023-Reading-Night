from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
import os
from models import db, User, bookreview, booknonje
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)

basdir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basdir, "bookdata.db")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'
app.config['JSON_AS_ASCII'] = False
engine = create_engine('sqlite:///bookdata.db')
Session = sessionmaker(bind=engine)
sql_session = Session()

db.init_app(app)
db.app = app

with app.app_context():
    db.create_all()

reviews = []

@app.route('/generic')
def generic():
    return render_template('generic.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 비밀번호 암호화
        hashed_password = generate_password_hash(password, method='sha256')
        # DB에 저장
        with app.app_context():
            user = User(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
        return redirect('/')
    return render_template('signup.html')

# 로그인 페이지
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # DB에서 유저 정보 가져오기
        user = User.query.filter_by(username=username).first()
        # 비밀번호 검증
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect('/main')
        else:
            return render_template('login.html')
    return render_template('login.html')

# 메인 페이지
@app.route('/main')
def main_page():
    if 'user_id' in session:
        with app.app_context():
            user = User.query.filter_by(id=session['user_id']).first()
        return render_template('main.html', user=user)
    else:
        return redirect('/')

@app.route('/index')
def index():
    return render_template('review_form.html')


@app.route('/')
def _index():
    # 리뷰 양식을 렌더링
    return render_template('review_form.html')


@app.route('/submit_review', methods=['GET', 'POST'])
def submit_review():
    if request.method == 'POST':
        # 양식 데이터 가져오기
        title = request.form['title']
        author = request.form['author']
        review = request.form['review']
        book = bookreview(title=title, author=author, review=review)
        db.session.add(book)
        db.session.commit()
        # 리뷰를 목록에 추가
        reviews.append({'title': title, 'author': author, 'review': review})
        # 리뷰 목록 페이지로 리디렉션
        return redirect(url_for('review_list'))

    # 요청 방법이 GET인 경우 검토 양식 렌더링
    return render_template('review_form.html')


@app.route('/reviews', methods=['GET', 'POST'])
def review_list():
    # 데이터베이스에서 모든 리뷰 검색
    reviews = bookreview.query.all()
    # 리뷰 데이터로 리뷰 목록 템플릿 렌더링
    return render_template('review_list.html', reviews=reviews)


@app.route('/next_page')
def next_page():
    return redirect(url_for('submit_review'))


@app.route('/list_page')
def list_page():
    return redirect(url_for('review_list'))


#########
nposts = []


@app.route('/nonje', methods=['GET', 'POST'])
def nonje():
    if request.method == 'POST':
        # 양식 데이터 가져오기
        num = request.form['num']
        content = request.form['content']
        nbook = booknonje(num=num, content=content)
        db.session.add(nbook)
        db.session.commit()
        # 리뷰를 목록에 추가
        nposts.append({'num': num, 'content': content})

        # Retrieve the values from the database
        values = db.query.first()

        # Convert the values to a JSON response
        response = {'num': values.num, 'content': values.content}
        return jsonify(response)
        # 리뷰 목록 페이지로 리디렉션
        return redirect(url_for('posts'))

    # 요청 방법이 GET인 경우 검토 양식 렌더링
    return render_template('nonje.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    # 데이터베이스에서 모든 리뷰 검색
    nposts = bookreview.query.all()
    # 리뷰 데이터로 리뷰 목록 템플릿 렌더링
    return render_template('nonje.html', nposts=nposts)


#########

@app.before_first_request
def create_database():
    db.create_all()
    #for data in bookreview.query.all():
         #db.session.delete(data)
    db.session.commit()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

# zz