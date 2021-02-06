import os
from utils import get_env_variable

POSTGRES_URL = get_env_variable('POSTGRES_URL')
POSTGRES_USER = get_env_variable('POSTGRES_USER')
POSTGRES_PASSWORD = get_env_variable('POSTGRES_PASSWORD')
POSTGRES_DB = get_env_variable('POSTGRES_DB')

SITE_DOMAIN = get_env_variable('SITE_DOMAIN')
SITE_PROTOCOL = get_env_variable('SITE_PROTOCOL')
SITE_PORT = get_env_variable('SITE_PORT')


class Config(object):
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    BROKER_URL = CELERY_BROKER_URL

    DEBUG = False
    TESTING = False
    # SQLAlchemy
    uri_template = 'postgresql://{user}:{pw}@{url}/{db}'
    SQLALCHEMY_DATABASE_URI = uri_template.format(
        user=POSTGRES_USER,
        pw=POSTGRES_PASSWORD,
        url=POSTGRES_URL,
        db=POSTGRES_DB)

    # Silence the deprecation warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    FLASK_ENV = 'development'
    DEBUG = True


class TestConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    # production config
    pass


def get_config(env=None):
    if env is None:
        try:
            env = os.environ['ENV']
        except Exception:
            env = 'development'
            print('env is not set, using env:', env)

    if env == 'production':
        return ProductionConfig()
    elif env == 'test':
        return TestConfig()

    return DevelopmentConfig()
