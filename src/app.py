from flask import Flask
from models import db
from config import get_config


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    db.init_app(app)
    return app
