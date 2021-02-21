from datetime import date, datetime

from flask import redirect, url_for
from flask.cli import FlaskGroup
from flask_login import LoginManager

from api_creator import create_api
from app_creator import create_app
from flask_migrate import Migrate
from celery_creator import create_celery
from models import db, UrlModel, User
from celery.utils.log import get_task_logger

# flask
from routes import short

app = create_app()

app.register_blueprint(short)

migrate = Migrate(app, db)

# Celery
logger = get_task_logger(__name__)
celery = create_celery()

# API
api = create_api(app)

# custom commands handler
cli = FlaskGroup(app)


# FLASK login
def user_loader(user_id):
    return User.query.get(user_id)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(user_loader)
login_manager.login_view = 'short.login'


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('short.index'))


@cli.command('test')
def run():
    print("It's working")


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

    # create admin user
    user = User(email="admin@admin.com", password="password123")
    db.session.add(user)
    db.session.commit()


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
