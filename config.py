import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'python.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = '*******@qq.com'
    MAIL_PASSWORD = '*********'
    MAIL_DEFAULT_SENDER = '********@qq.com'
    FLASK_ADMIN = 'wubo@paicaifu.com'


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig}
