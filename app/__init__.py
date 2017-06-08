from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import config
from flask_login import LoginManager
from flask_mail import Mail
from flask_pagedown import PageDown

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
pagedown = PageDown()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    # 附加路由和自定义的错误页面 return app
    from .main import main as mn
    app.register_blueprint(mn)
    from .auth import auth as ab
    app.register_blueprint(ab, url_prefix='/auth')
    login_manager.init_app(app)
    pagedown.init_app(app)
    return app
