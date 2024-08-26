from celery import Celery

celery_app = Celery(
    __name__,
    broker='redis://localhost:6380/0',
    backend='redis://localhost:6380/0',
    include=['app.celery_settings.tasks']
)

# import app.celery_settings.tasks

celery_app.conf.beat_schedule = {
    'check-stock-status-every-hour': {
        'task': 'app.celery_settings.tasks.check_stock_status',
        'schedule': 3600.0,
    },
    'check-request-every-hour': {
        'task': 'app.celery_settings.tasks.check_pending_request',
        'schedule': 300
    }
}


@celery_app.task
def add(x: int, y: int):
    return x + y


# command to run beat
# celery -A app.celery_settings beat --loglevel=info
