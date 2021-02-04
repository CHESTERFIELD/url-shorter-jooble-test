import os


class Config(object):
    DEBUG = False
    TESTING = False
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/jooble_project"

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
