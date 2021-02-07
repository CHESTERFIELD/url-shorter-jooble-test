from flask import Flask
from models import db
from config import get_config


def create_app(env=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(get_config(env))
    db.init_app(app)
    return app
