from celery import shared_task
from schedule_parsing.parsing import Parsing

@shared_task
def upload_schedule(file:str, start_row: int, department: str, date_start, date_end, day):
    parse = Parsing(filename=file, start_row=start_row)
    start = parse.start(department, date_start, date_end, day)
    return start