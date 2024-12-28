from loguru import logger
from schedule_parsing.event import Event


class TestScheduleTable:
    """ Тестируем класс ScheduleTable """

    def test_add_event_to_schedule_table(self, schedule, schedule_event):
        """ Проверяем корректное добавление события в расписание """
        schedule.add_event_to_schedule_table(schedule_event)
        assert 'ИСиП-24 (11 кл.)' in schedule.schedule
        assert '1 пара' in schedule.schedule['ИСиП-24 (11 кл.)']
        events_list = schedule.schedule['ИСиП-24 (11 кл.)']['1 пара']
        assert len(events_list) == 1
        assert events_list[0]["discipline"] == 'Разработка мобильных приложений'
        assert events_list[0]["teacher"] == 'Кузнецов Кирилл Александрович'
        assert events_list[0]["auditory"] == '402'

    def test_count_group_empty(self, schedule):
        """ Проверяем метод count_group для пустого расписания """
        assert schedule.count_group() == 0

    def test_count_group_after_add(self, schedule, schedule_event):
        """ Проверяем, что count_group возвращает корректное значение после добавления """
        schedule.add_event_to_schedule_table(schedule_event)
        assert schedule.count_group() == 1

    def test_multiple_events_same_group_diff_couples(self, schedule, schedule_event):
        """ Добавляем несколько Event в ту же группу, но разные пары """
        schedule.add_event_to_schedule_table(schedule_event)
        another_event = Event(
            group=schedule_event.group,
            couple='2 пара',
            discipline='Информатика',
            teacher='Иванов Иван Иванович',
            auditory='202'
        )
        schedule.add_event_to_schedule_table(another_event)

        assert 'ИСиП-24 (11 кл.)' in schedule.schedule
        assert '1 пара' in schedule.schedule["ИСиП-24 (11 кл.)"]
        assert '2 пара' in schedule.schedule["ИСиП-24 (11 кл.)"]
        assert len(schedule.schedule["ИСиП-24 (11 кл.)"]["1 пара"]) == 1
        assert len(schedule.schedule["ИСиП-24 (11 кл.)"]["2 пара"]) == 1

    def test_multiple_events_same_group_same_couple(self, schedule, schedule_event):
        """
        Добавляем несколько Event в ту же группу и ту же пару.
        Ожидается, что для пары формируется список.
        """
        schedule.add_event_to_schedule_table(schedule_event)
        logger.error(schedule.schedule)
        another_event = Event(
            group=schedule_event.group,
            couple=schedule_event.couple,
            discipline='Разработка программного обеспечения',
            teacher='Иванов Иван Иванович',
            auditory='403'
        )
        schedule.add_event_to_schedule_table(another_event)
        logger.error(schedule.schedule)
        events_list = schedule.schedule["ИСиП-24 (11 кл.)"]["1 пара"]
        logger.warning(events_list)
        logger.error(schedule.schedule)
        assert len(events_list) == 2

        disciplines = {ev["discipline"] for ev in events_list}
        teachers = {ev["teacher"] for ev in events_list}
        auditories = {ev["auditory"] for ev in events_list}

        assert 'Разработка мобильных приложений' in disciplines
        assert 'Разработка программного обеспечения' in disciplines
        assert 'Кузнецов Кирилл Александрович' in teachers
        assert 'Иванов Иван Иванович' in teachers
        assert '402' in auditories
        assert '403' in auditories

    def test_add_event_no_duplicates(self, schedule, schedule_event):
        """ Проверяем что не создаются одинаковые пары """
        schedule_event = schedule_event
        schedule_event_2 = schedule_event

        schedule.add_event_to_schedule_table(schedule_event)
        schedule.add_event_to_schedule_table(schedule_event_2)

        assert len(schedule.schedule["ИСиП-24 (11 кл.)"]["1 пара"]) == 1
        assert schedule.schedule["ИСиП-24 (11 кл.)"]["1 пара"][0]["discipline"] == 'Разработка мобильных приложений'
        assert schedule.schedule["ИСиП-24 (11 кл.)"]["1 пара"][0]["teacher"] == 'Кузнецов Кирилл Александрович'
        assert schedule.schedule["ИСиП-24 (11 кл.)"]["1 пара"][0]["auditory"] == '402'
