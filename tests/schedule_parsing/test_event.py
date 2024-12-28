import pytest
from schedule_parsing.event import Event


class TestScheduleParsingEvent:

    def test_event_creation(self, schedule_event):
        """ Проверяем инициализацию объекта event """
        assert schedule_event.auditory == '402'
        assert schedule_event.teacher == 'Кузнецов Кирилл Александрович'
        assert schedule_event.discipline == 'Разработка мобильных приложений'
        assert schedule_event.couple == '1 пара'
        assert schedule_event.group == 'ИСиП-24 (11 кл.)'

    def test_event_str_representation(self, schedule_event):
        """ Проверяем метод __str__ """
        event_str = str(schedule_event)
        assert 'ИСиП-24 (11 кл.)' in event_str
        assert '1 пара Разработка мобильных приложений / Кузнецов Кирилл Александрович 402' in event_str

    def test_event_to_dict(self, schedule_event):
        """ Проверяем метод to_dict """
        event_dict = schedule_event.to_dict()
        assert event_dict['group'] == 'ИСиП-24 (11 кл.)'
        assert event_dict['couple'] == '1 пара'
        assert event_dict['discipline'] == 'Разработка мобильных приложений'
        assert event_dict['teacher'] == 'Кузнецов Кирилл Александрович'
        assert event_dict['auditory'] == '402'

    @pytest.mark.parametrize('sut, expected', [
        ('ИСиП-23 (9 кл.)', 'ИСиП-23 (9 кл.)'),
        (' ИСиП-23 (9 кл.)', 'ИСиП-23 (9 кл.)'),
        ('ИСиП-23 (9 кл.) ', 'ИСиП-23 (9 кл.)')
    ])
    def test_name_group(self, sut, expected):
        """ Проверяем установку разных названий групп при инициализации event """
        event = Event(group=sut, couple='1 пара', discipline='ОБЖ', teacher='Иванов Александр', auditory='402')
        assert event.group == expected

    @pytest.mark.parametrize('sut, expected', [('1 пара', '1 пара'), (' 1 пара', '1 пара'), ('1 пара ', '1 пара')])
    def test_number_couple(self, sut, expected):
        event = Event(group='С-23 (9кл.)', couple=sut, discipline='ОБЖ', teacher='Иванов Александр', auditory='402')
        assert event.couple == expected

    @pytest.mark.parametrize('sut, expected', [('ОБЖ', 'ОБЖ'), (' ОБЖ', 'ОБЖ'), ('ОБЖ ', 'ОБЖ')])
    def test_name_discipline(self, sut, expected):
        event = Event(group='С-23 (9кл.)', couple='1 пара', discipline=sut, teacher='Иванов Александр', auditory='402')
        assert event.discipline == expected

    @pytest.mark.parametrize('sut, expected', [
        ('Кузнецов Кирилл Александрович', 'Кузнецов Кирилл Александрович'),
        (' Кузнецов Кирилл Александрович', 'Кузнецов Кирилл Александрович'),
        ('Кузнецов Кирилл Александрович ', 'Кузнецов Кирилл Александрович')
    ])
    def test_teacher_name(self, sut, expected):
        event = Event(group='С-23 (9кл.)', couple='1 пара', discipline='ОБЖ', teacher=sut, auditory='402')
        assert event.teacher == expected

    @pytest.mark.parametrize('teacher_name', ['John Middle Doe Extra', 'Ivan', ])
    def test_event_teacher_name_invalid(self, teacher_name):
        """ Проверяем, что при некорректном количестве слов вызывается ValueError """
        with pytest.raises(ValueError):
            Event(group='C-33', couple='1 пара', discipline='ОБЖ', teacher=teacher_name, auditory='101')

    @pytest.mark.parametrize('teacher_name', ['None', 'none', 'NONE',])
    def test_event_teacher_is_none(self, teacher_name):
        """ Проверяем сценарий, когда преподаватель в строке 'none'/'None'. """
        event = Event(group='С-33 (9 кл.)', couple='1 пара', discipline='ОБЖ', teacher=teacher_name, auditory='302')
        assert event.teacher == 'None None None'

    @pytest.mark.parametrize('sut_name', ['Кузнецов Кирилл Александрович Александрович'])
    def test_no_valid_teacher_name(self, sut_name):
        with pytest.raises(ValueError):
            Event(group='С-23 (9кл.)', couple='1 пара', discipline='ОБЖ', teacher=sut_name, auditory='402')

    @pytest.mark.parametrize('sut, expected', [('402', '402'), (' 40', '40'), ('40 ', '40'), (' none ', 'none')])
    def test_number_auditory(self, sut, expected):
        event = Event(group='С-23 (9кл.)', couple='1 пара', discipline='ОБЖ', teacher='Иванов Александр', auditory=sut)
        assert event.auditory == expected
