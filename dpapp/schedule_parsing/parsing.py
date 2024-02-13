"""
Copyright (c) 2022-2024 schedule parsing
Development @KirillKuznetsov
Parsing 10.02.2024
"""

import openpyxl, datetime
from .schedule import Schedule
from .schedule_event import ScheduleEvent
from django.conf import settings


class Parsing:
    # TODO: Добавить многопоточность
    path = settings.MEDIA_ROOT + 'xls/schedule/'

    def __init__(self, filename: str, department: str, date: datetime.date):
        self.file = openpyxl.open(self.path + filename, read_only=True).active
        self.table_row = 1
        self.table_col = 1
        self.department = department
        self.date = date
        self.schedule = Schedule(from_date=date, department=self.department)
        self.max_col = self.file.max_column
        self.errors = []

    def parse(self):
        # TODO: Изменить формат хранения на JSON
        while self.table_col < self.file.max_column:
            for row in range(2, self.file.max_row + 1):
                current_coordinate = self.file[row][self.table_col].coordinate

                if self.file[row][self.table_col].value is not None:

                    group = self.file[1][self.table_col].value.strip()
                    couple = self.file[row][0].value.strip()
                    auditory = str(self.file[row][self.table_col + 1].value).strip()
                    discipline = self.file[row][self.table_col].value.split('/', 1)[0].strip()
                    teacher = self.file[row][self.table_col].value.split('/')[1].strip()

                    event = ScheduleEvent(group, couple, auditory, discipline, teacher)
                    self.schedule.add_event(event)
                    print(current_coordinate, event)
                else:
                    print(current_coordinate, 'empty')
            self.table_col += 2

        print(self.schedule.display_schedule())
        return True if self.errors.__len__() == 0 else False

    def save_change(self):
        pass

    def save_base(self):
        pass


