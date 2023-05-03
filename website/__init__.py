from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail, Message
import datetime



db = SQLAlchemy()
DB_NAME = "daaaataaabassseeee.db"
mail = Mail()


def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Jesus is love'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    from .action import action
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(action, url_prefix='/')
    
    from .models import Blacklist, User, Events, Year, Signup, Basic, Older, Winter, Person, Turnament

    with app.app_context():
        db.create_all()

    from modules.check_module import check_date

    with app.app_context():
        check_date()

    
    login_manager = LoginManager()
    login_manager.login_view = 'views.home'
    login_manager.login_message = 'Dostęp do strony tylko po zalogowaniu'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'kapszlaksend@gmail.com'
    app.config['MAIL_PASSWORD'] = 'fimyklgnxqvdleti'

    mail = Mail(app)
 
    
    return app

