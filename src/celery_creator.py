from celery import Celery
from celery.schedules import crontab


def create_celery(app):
    """Celery instantiation."""

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