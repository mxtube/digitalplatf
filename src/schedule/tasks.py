from celery import shared_task
from schedule_parsing.parsing import Parsing


@shared_task
def upload_schedule(file: str, start_row: int, department: str, date_start: str, date_end: str, day: str):
    parse = Parsing(filename=file, start_row=start_row, department=department)
    start = parse.start(date_start, date_end, day)
    return True if start else False
