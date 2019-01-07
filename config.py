# config.py

import os


class Config:
    """
    Common configurations
    """

    SECRET_KEY = os.environ.get('SECRET_KEY', 'some value')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgresql://db_user:password@localhost/user_crud_db')

    TESTING = False
    DEBUG = False
    CSRF_ENABLED = True  # protect against CSRF attacks
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """
    Testing configurations
    """

    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
