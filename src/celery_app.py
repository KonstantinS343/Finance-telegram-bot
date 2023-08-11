from celery import Celery

from config import CELERY_HOST, CELERY_PORT


celery = Celery('executor', broker=f'redis://{CELERY_HOST}:{CELERY_PORT}', include=['report.table',
                                                                                    'report.email_send'])


celery.conf.task_serializer = 'pickle'
celery.conf.accept_content = ['application/json', 'application/x-python-serialize']
