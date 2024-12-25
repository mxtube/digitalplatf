import pytest
from schedule_parsing.event import Event


class TestScheduleParsingEvent:

    def test_event_creation(self, schedule_event):
        assert schedule_event.auditory == '402'
        assert schedule_event.teacher == 'Кузнецов Кирилл Александрович'
        assert schedule_event.discipline == 'Разработка мобильных приложений'
        assert schedule_event.couple == '1 пара'
        assert schedule_event.group == 'ИСиП-24 (11 кл.)'


    @pytest.mark.parametrize('sut, expected', [
        ('ИСиП-23 (9 кл.)', 'ИСиП-23 (9 кл.)'),
        (' ИСиП-23 (9 кл.)', 'ИСиП-23 (9 кл.)'),
        ('ИСиП-23 (9 кл.) ', 'ИСиП-23 (9 кл.)')
    ])
    def test_name_group(self, sut, expected):
        event = Event(
            group=sut,
            couple='1 пара',
            discipline='ОБЖ',
            teacher='Иванов Александр',
            auditory='402'
        )
        assert event.group == expected

    @pytest.mark.parametrize('sut, expected', [('1 пара', '1 пара'), (' 1 пара', '1 пара'), ('1 пара ', '1 пара')])
    def test_number_couple(self, sut, expected):
        event = Event(
            group='С-23 (9кл.)',
            couple=sut,
            discipline='ОБЖ',
            teacher='Иванов Александр',
            auditory='402'
        )
        assert event.couple == expected

    @pytest.mark.parametrize('sut, expected', [('ОБЖ', 'ОБЖ'), (' ОБЖ', 'ОБЖ'), ('ОБЖ ', 'ОБЖ')])
    def test_name_discipline(self, sut, expected):
        event = Event(
            group='С-23 (9кл.)',
            couple='1 пара',
            discipline=sut,
            teacher='Иванов Александр',
            auditory='402'
        )
        assert event.discipline == expected

    @pytest.mark.parametrize('sut, expected', [
        ('Кузнецов Кирилл Александрович', 'Кузнецов Кирилл Александрович'),
        (' Кузнецов Кирилл Александрович', 'Кузнецов Кирилл Александрович'),
        ('Кузнецов Кирилл Александрович ', 'Кузнецов Кирилл Александрович')
    ])
    def test_teacher_name(self, sut, expected):
        event = Event(
            group='С-23 (9кл.)',
            couple='1 пара',
            discipline='ОБЖ',
            teacher=sut,
            auditory='402'
        )
        assert event.teacher == expected

    @pytest.mark.parametrize('sut_name', ['Кузнецов Кирилл Александрович Александрович'])
    def test_no_valid_teacher_name(self, sut_name):
        with pytest.raises(ValueError):
            event = Event(
                group='С-23 (9кл.)',
                couple='1 пара',
                discipline='ОБЖ',
                teacher=sut_name,
                auditory='402'
            )


    @pytest.mark.parametrize('sut, expected', [('402', '402'), ('40', '40'), ('40 ', '40')])
    def test_number_auditory(self, sut, expected):
        event = Event(
            group='С-23 (9кл.)',
            couple='1 пара',
            discipline='ОБЖ',
            teacher='Иванов Александр',
            auditory=sut
        )
        assert event.auditory == expected
