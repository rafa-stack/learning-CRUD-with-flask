import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'rahasia-rafa'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'berita.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
