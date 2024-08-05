import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.urandom(24)
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)


class DevelopmentConfig(Config):
    DEBUG = True
    ENVIRONMENT = 'development'
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = False


class ProductionConfig(Config):
    DEBUG = False
    ENVIRONMENT = 'production'
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
