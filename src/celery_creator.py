from celery import Celery
from celery.schedules import crontab

from app_creator import create_app


def create_celery(app=None):
    """Celery instantiation."""
    app = create_app()
    celery = Celery(app, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    print(app.config['CELERY_RESULT_BACKEND'])
    app.config['CELERYBEAT_SCHEDULE'] = {
        # Executes every minute
        'periodic_task-every-minute': {
            'task': 'delete_expired_urls',
            'schedule': crontab(minute="*")
        }
    }
    celery.conf.update(app.config)

    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

    return celery
