from celery import shared_task
from schedule_parsing.parsing import Parsing

@shared_task(task_name='1111')
def upload_schedule(file:str, start_row: int, department: str, date_start, date_end, day):
    parse = Parsing(filename=file, start_row=start_row, department=department)
    start = parse.start(date_start, date_end, day)
    return start