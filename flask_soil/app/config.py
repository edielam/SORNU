import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-secret-key'
    #SQLALCHEMY_DATABASE =os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
