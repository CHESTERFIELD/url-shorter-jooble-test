from flask import Flask
from models import db
from config import get_config


def create_app():
    app = Flask(__name__)
    from config import DevelopmentConfig
    app.config['FLASK_ENV'] = 'development'
    # app.config.from_object(DevelopmentConfig)
    app.config.from_object(get_config())
    db.init_app(app)
    return app
