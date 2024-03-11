"""
Created on Thu 7.03.24
@author: Kirill Kuznetsov
"""

import openpyxl
from .schedule import Schedule
from .event import Event
from core.settings import MEDIA_ROOT


class Parsing(Schedule, Event):

    EXCEL_FILE_PATH = MEDIA_ROOT + 'xls/schedparsing/'

    def __init__(self, filename: str):
        self.file = openpyxl.open(self.EXCEL_FILE_PATH + filename, read_only=True).active
        self.current_col = 1
        self.start_row = 2
        self.error_box = []
        self.schedule = Schedule()

    def start(self):
        if self.__excel_reader():
            self.__save_db()

    def __excel_reader(self):
        while self.current_col < self.file.max_column:
            group = self.file[1][self.current_col].value.strip()
            for file_row in range(self.start_row, self.file.max_row + 1):
                if self.file[file_row][self.current_col].value is not None:
                    stream = self.file[file_row][0].value.strip()
                    discipline = self.file[file_row][self.current_col].value.split('/')[0].strip()
                    teacher = self.file[file_row][self.current_col].value.split('/')[1].strip()
                    auditory = str(self.file[file_row][self.current_col + 1].value).strip()
                    event = Event(group, stream, discipline, teacher, auditory)
                    self.schedule.add_event(event)
            self.current_col += 2
        else:
            return True

    def __save_db(self):
        pass
