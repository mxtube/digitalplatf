import pytest
from schedule_parsing.event import Event
from schedule_parsing.parsing import ParsingFile
from schedule_parsing.schedule_table import ScheduleTable


@pytest.fixture
def schedule_event():
    event = Event(
        group='ИСиП-24 (11 кл.)',
        couple='1 пара',
        discipline='Разработка мобильных приложений',
        teacher='Кузнецов Кирилл Александрович',
        auditory='402'
    )
    return event


@pytest.fixture
def tmp_correct_sch_file_by_day(department):
    file = ParsingFile(
        filepath='./tests/schedule_parsing/tmp_schedule_correct_by_day.xlsx',
        start_row=2,
        department=department.name,
    )
    return file


@pytest.fixture
def schedule():
    """ Фикстура для создания пустой расписания (ScheduleTable). """
    return ScheduleTable()
