from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail, Message
import pdfkit


db = SQLAlchemy()
DB_NAME = "dbneewew.db"
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

    from .models import Blacklist, User, EventsNew, SignUpData, Events, Year, Template1, Template2, Template3 

    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'views.home'
    login_manager.login_message = 'Dostęp do strony tylko po zalogowaniu'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'kapszlaksend@gmail.com'
    app.config['MAIL_PASSWORD'] = 'fimyklgnxqvdleti'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail.init_app(app)
    #config = pdfkit.configuration(wkhtmltopdf="C:/Users/wojto/Documents/Piotrek/kap_zapisy/website/static/bin")
    
    return app

