from flask_restful import Api

from app import create_app
from flask_migrate import Migrate
from models import db
from repositories.url import UrlRepository
from resources.url import UrlAPI
from flask import redirect
from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger

app = create_app()
logger = get_task_logger(__name__)

migrate = Migrate(app, db)


def make_celery():
    """Celery instantiation."""
    app = create_app()

    # Celery instance creation
    celery = Celery(__name__)
    app.config['CELERYBEAT_SCHEDULE'] = {
        # Executes every minute
        'periodic_task-every-minute': {
            'task': 'periodic_task',
            'schedule': crontab(minute="*")
        }
    }

    # Celery Configuration
    celery.conf.update(app.config)

    return celery

celery = make_celery()

print(app.config)



@app.cli.command('test')
def run():
    print("It's working")


@app.route('/<short_url>')
def hello_world(short_url):
    url = UrlRepository.get(url_hash=short_url)
    return redirect(url.full_url), 301


@celery.task(name="periodic_task")
def periodic_task():
    print('Hi! from periodic_task')
    logger.info("Hello! from periodic task")


# API
api = Api(app)
api.add_resource(UrlAPI, '/api/v1/url')
