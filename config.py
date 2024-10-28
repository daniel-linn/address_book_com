import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    
## Default admin account(no space)
## username: admin
## password: admin