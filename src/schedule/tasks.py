from celery import shared_task
from schedule_parsing.parsing import Parsing

@shared_task()
def upload_schedule():
    pass