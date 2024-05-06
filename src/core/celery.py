import os
from celery import Celery
from django_celery_results.apps import CeleryResultConfig

CeleryResultConfig.verbose_name = "Задачи"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
