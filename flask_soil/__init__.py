from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flask_soil.app.config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = '57d46dadbd894e7db6c0d3bfd6df64ccf24d80bd5e'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///user_data.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager= LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flask_soil import routes
