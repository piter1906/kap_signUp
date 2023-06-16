from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail, Message
import datetime
from dotenv import load_dotenv
import os
import logging


db = SQLAlchemy()
mail = Mail()
load_dotenv()


def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    db.init_app(app)

    logging.basicConfig(filename='website/app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s : %(message)s')

    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.ERROR)
    
    from .views import views
    from .auth import auth
    from .action import action
    from .error import error
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(action, url_prefix='/')
    app.register_blueprint(error, url_prefix='/')
    
    from .models import Blacklist, User, Events, Year, Signup, Basic, Older, Winter, Person, Turnament

    with app.app_context():
        db.create_all()


    from modules.check_module import check_date

    with app.app_context():
        check_date()

    
    login_manager = LoginManager()
    login_manager.login_view = 'views.home'
    login_manager.login_message = 'Dostęp do strony tylko po zalogowaniu.'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USER')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    mail = Mail(app)
 
    
    return app

