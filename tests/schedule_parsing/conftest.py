import pytest
from schedule_parsing.event import Event


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