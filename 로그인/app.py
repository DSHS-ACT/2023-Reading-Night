from flask import Flask, render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, User

app = Flask(__name__, template_folder='C:/Users/82107/Desktop/templates')
app.secret_key = 'some secret key'

# DB 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/82107/Desktop/templates/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
        db.create_all()
        
# 회원가입 페이지
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
def main():
    if 'user_id' in session:
        with app.app_context():
            user = User.query.filter_by(id=session['user_id']).first()
        return render_template('main.html', user=user)
    else:
        return redirect('/')
        
if __name__ == '__main__':
    app.run(debug=True)
