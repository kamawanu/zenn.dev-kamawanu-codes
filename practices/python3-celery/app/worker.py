# celery.py
from celery import Celery
import os
# worker-1  | [2024-10-19 12:09:39,724: ERROR/MainProcess] Received unregistered task of type 'tasks.add'.
# worker-1  | The message has been ignored and discarded.
import tasks

broker_url = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')

app = Celery('celery_demo',
             broker=broker_url,
             backend=result_backend)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
