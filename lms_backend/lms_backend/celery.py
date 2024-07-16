import os

from celery import Celery
from kombu import Queue
from time import sleep
from datetime import timedelta
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_backend.settings')

app = Celery('lms_backend', broker_connection_retry_on_startup=True)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.task_queues = (
    Queue('default',routing_key='task.default'),
    Queue('high_priority', routing_key='task.high_priority'),
    Queue('low_priority', routing_key='task.low_priority'),
)

app.conf.beat_schedule = {
    'reject_unpaid_requests':{
        'task':'reject_book_request',
        'schedule':crontab(day_of_week=0, hour=5, minute=30),
    },
    'stock_check_periodic':{
        'task':'stock_check',
        'schedule':crontab(hour=0, minute=0),
        'args':['weekly checking'],
        'kwargs':{'recipient':'abhishekwagh420@gmail.com'},
        'options':{'queue': 'high_priority'}
    },
    'show_recent_logins': {
        'task': 'show_recent_logins',
        'schedule': crontab(minute=5,hour='*'), 
        'options':{'queue':'low_priority'}
    },
}

app.conf.task_time_limit = 50
app.conf.task_soft_limit_limit = 40  #SoftTimeLimitExceeded error

app.conf.worker_concurrency = 4 
app.conf.worker_max_tasks_per_child = 100 

app.autodiscover_tasks()

#  Make sure that your Celery worker is started with the -B option to enable the Celery Beat scheduler.



