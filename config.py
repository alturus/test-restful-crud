import os
from datetime import timedelta
from flask_dotenv import DotEnv

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_precious_secret_key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-string')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ERROR_MESSAGE_KEY = 'message'
    ADMIN_USERNAME = None
    ADMIN_PASSWORD = None

    @classmethod
    def init_app(cls, app):
        env = DotEnv()
        env.init_app(app)


class DevelopmentConfig(Config):
    DEBUG = True
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'password')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI',
                                             'sqlite:///' + os.path.join(basedir, 'books.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI',
                                             'sqlite:///' + os.path.join(basedir, 'books_test.db'))
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=5)


class ProductionConfig(Config):
    DEBUG = False
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', None)
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', None)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI',
                                             'sqlite:///' + os.path.join(basedir, 'books.db'))


config = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)
