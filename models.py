from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))

class Berita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(200))
    isi = db.Column(db.Text)
