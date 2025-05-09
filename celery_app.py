import os
from celery import Celery

broker_url = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')

celery_app = Celery(
    'itarch',
    broker=broker_url,
    backend=result_backend,
    include=['tasks']
)

celery_app.conf.update(
    task_track_started=True,
    task_time_limit=300
)