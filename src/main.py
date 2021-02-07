from datetime import date, datetime

from flask.cli import FlaskGroup
from api_creator import create_api
from app_creator import create_app
from flask_migrate import Migrate
from celery_creator import create_celery
from models import db, UrlModel
from repositories.url import UrlRepository
from flask import redirect
from celery.utils.log import get_task_logger

# flask
app = create_app()

migrate = Migrate(app, db)

# Celery
logger = get_task_logger(__name__)
celery = create_celery()

# API
api = create_api(app)

# custom commands handler
cli = FlaskGroup(app)


@cli.command('test')
def run():
    print("It's working")


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@app.route('/<short_url>')
def hello_world(short_url):
    url = UrlRepository.get(url_hash=short_url)
    return redirect(url.full_url), 301


@celery.task(name="delete_expired_urls")
def delete_expired_urls():
    logger.info("started delete_expired_urls")
    if datetime.now().time() != '00:00':
        return False

    count = 0
    expired_urls = UrlModel.query.filter(UrlModel.expire_date < date.today()).all()
    for url in expired_urls:
        db.session.delete(url)
        db.session.commit()
        count += 1

    logger.info("finished delete_expired_urls: delete {} urls".format(count))

    return True


if __name__ == "__main__":
    cli()
