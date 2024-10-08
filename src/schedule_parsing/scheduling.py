"""
Created on Thu 7.03.24
@author: Kirill Kuznetsov
"""

import datetime
import json
from core.settings import MEDIA_ROOT


class Scheduling:
    """ Класс хранящий расписание для парсинга """

    JSON_PATH = MEDIA_ROOT + 'json/schedparsing/'
    IMAGE_PATH = MEDIA_ROOT + 'pix/schedparsing/'

    def __init__(self):
        self.schedule = {}

    def add_event(self, event):
        """ Метод добавления элемента расписания в общий словарь с расписанием. """
        event = event.__dict__
        if self.__has_group(event.get('group')):
            if self.__add_couple(event.get('group'), event.get('couple')):
                self.schedule[event.get('group')][event.get('couple')] += [
                    {
                        "discipline": event.get('discipline'),
                        "teacher": event.get('teacher'),
                        "auditory": event.get('auditory')
                    }
                ]
        return self.schedule

    def __add_couple(self, group, couple):
        """ Метод проверки номера пары в учебной группе. Если такой пары нет, добавляет. """
        if couple not in self.schedule.get(group):
            self.schedule[group][couple] = []
        return True

    def __has_group(self, group):
        """ Метод проверки группы в расписании. Если такой нет, вызывает функцию добавления. """
        return self.__add_group(group) if group not in self.schedule.keys() else True

    def __add_group(self, group):
        """ Метод добавления новой группы в расписание. """
        before = self.count_group() + 1
        self.schedule[group] = {}
        return len(self.schedule.keys()) - before == 1

    def count_group(self):
        """ Метод получения кол-ва групп в расписании """
        return len(self.schedule.keys())

    def display_schedule(self):
        """ Метод получения расписания """
        return self.schedule

    def save_to_json(self):
        """ Метод сохранения расписания в JSON """
        now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        with open(self.JSON_PATH + now + '.json', 'w', encoding='utf-8') as f:
            json.dump(self.schedule, f, ensure_ascii=False, indent=4)

