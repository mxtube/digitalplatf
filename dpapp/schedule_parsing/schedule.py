"""
Created on Thu 7.03.24
@author: Kirill Kuznetsov
"""

import datetime
import json
from core.settings import MEDIA_ROOT


class Schedule:

    JSON_PATH = MEDIA_ROOT + 'json/schedparsing/'
    IMAGE_PATH = MEDIA_ROOT + 'pix/schedparsing/'

    def __init__(self):
        self.schedule = {}

    def add_event(self, event):
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
        if couple not in self.schedule.get(group):
            self.schedule[group][couple] = []
        return True

    def __has_group(self, group):
        return self.__add_group(group) if group not in self.schedule.keys() else True

    def __add_group(self, group):
        before = len(self.schedule.keys()) + 1
        self.schedule[group] = {}
        return True if len(self.schedule.keys()) - before == 1 else False

    def count_group(self):
        return len(self.schedule.keys())

    def display_schedule(self):
        return self.schedule

    def save_to_json(self):
        with open(self.JSON_PATH + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.json', 'w', encoding='utf-8') as f:
            json.dump(self.schedule, f, ensure_ascii=False, indent=4)

