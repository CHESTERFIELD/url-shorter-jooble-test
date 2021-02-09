from flask import Flask
from models import db


def create_app(env=None):
    app = Flask(__name__)
    if env == 'test':
        app.config.from_object("config.TestConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")
    db.init_app(app)
    return app
