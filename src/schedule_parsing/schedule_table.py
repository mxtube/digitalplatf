"""
Created on Thu 7.03.24
@author: Kirill Kuznetsov
"""
from typing import Dict
from .event import Event


class ScheduleTable:

    def __init__(self):
        self.schedule: Dict = {}

    def add_event_to_schedule_table(self, event: Event):
        """ Метод добавления элемента нового объекта в таблицу расписания """
        event_dict = event.to_dict()
        group = event_dict.get('group')
        couple = event_dict.get('couple')
        if self._has_group(group):
            if self._add_couple(group, couple):
                new_item = {
                    "discipline": event_dict.get('discipline'),
                    "teacher": event_dict.get('teacher'),
                    "auditory": event_dict.get('auditory')
                }
                current_events = self.schedule[group][couple]
                if new_item not in current_events:
                    current_events.append(new_item)
        return self.schedule

    def _add_couple(self, group, couple):
        """ Метод проверки номера пары в учебной группе. Если такой пары нет, добавляет """
        if couple not in self.schedule.get(group):
            self.schedule[group][couple] = []
        return True

    def _has_group(self, group):
        """ Метод проверки группы в расписании. Если такой нет, вызывает функцию добавления """
        return self._add_group(group) if group not in self.schedule.keys() else True

    def _add_group(self, group):
        """ Метод добавления новой группы в расписание. """
        self.schedule[group] = {}
        return True

    def count_group(self) -> int:
        """ Метод получения кол-ва групп в расписании """
        return len(self.schedule.keys())
