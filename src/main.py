from api import create_api
from app import create_app
from flask_migrate import Migrate
from celery_creator import create_celery
from models import db
from repositories.url import UrlRepository
from flask import redirect
from celery.utils.log import get_task_logger

app = create_app()
logger = get_task_logger(__name__)

migrate = Migrate(app, db)

# Celery
celery = create_celery(app)

# API
api = create_api(app)

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
