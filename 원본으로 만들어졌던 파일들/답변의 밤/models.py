from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

app = Flask(__name__)
db = SQLAlchemy()

    
basdir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basdir, "bookdata.db")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookdata.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'


class bookreview(db.Model):
    __tablename__ = "bookreview"  
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    review = db.Column(db.String(5000), nullable=False)
    
class booknonje(db.Model):
    __tablename__ = "booknonje"  
    
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.String(15), nullable=False)
    content = db.Column(db.String(1000), nullable=False)

class database(db.Model):
    __tablename__ = "database"  

    id = db.Column(db.Integer, primary_key=True)
    shop = db.Column(db.String(30))
    address = db.Column(db.String(50))
    sector = db.Column(db.String(10))
    menu = db.Column(db.String(255))
    latitude = db.Column(db.String(30))
    longitude = db.Column(db.String(30))
    title = db.Column(db.String(100), nullable=False)
    review = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text, nullable=False)
    num = db.Column(db.String(15), nullable=False)
    content = db.Column(db.String(1000), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    

@app.before_first_request
def create_database():
     db.create_all(app=app)
     db.session.commit()
