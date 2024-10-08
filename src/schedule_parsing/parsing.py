"""
Created on Thu 7.03.24
@author: Kirill Kuznetsov
"""
import openpyxl, re
from .event import Event
from loguru import logger
from .scheduling import Scheduling
from core.settings import MEDIA_ROOT
from educationpart.models import Studygroup
from college.models import Department, CustomPerson
from django.core.exceptions import ObjectDoesNotExist
from schedule.models import Schedule, GroupStream, Couple, Discipline, Auditory

# TODO: Убрать баг для обработки ошибки если в выбраном диапозоне дат нет выбранного дня

class Parsing(Scheduling, Event):

    EXCEL_FILE_PATH = MEDIA_ROOT + 'xls/schedparsing/'

    def __init__(self, filename: str, start_row: int, department: str):
        self.department = Department.objects.get(name=department)
        self.file = openpyxl.open(f'{self.EXCEL_FILE_PATH}{self.department.slug}/{filename}', read_only=True).active
        self.current_col = 1
        self.start_row = start_row
        self.error_box = []
        self.schedule = Scheduling()

    def start(self, start_date, end_date, weekday):
        """ Функция запуска парсинга данных из файла. Функция запускает 3 операции. """
        logger.info('Запущен парсинг расписания')
        if self.__excel_reader():
            if self.__check_data_db(self.department):
                groups: list = Schedule.get_date_by_range(start_date, end_date, weekday)
                self.__save_change_gb(self.department, groups)
        return self.error_box

    def __excel_reader(self):
        """ Функция чтения данных из файла. """
        logger.info('Чтение данных из файла')
        while self.current_col < self.file.max_column:
            group = self.file[1][self.current_col].value.strip()
            for file_row in range(self.start_row, self.file.max_row + 1):
                current_cell = self.file[file_row][self.current_col]
                if current_cell.value is not None:
                    try:
                        stream = self.__parse_stream(self.file[file_row][0])
                        discipline = self.__parse_discipline(self.file[file_row][self.current_col])
                        teacher = self.__parse_teacher(self.file[file_row][self.current_col])
                        auditory = self.__parse_auditory(self.file[file_row][self.current_col + 1])
                        event = Event(group, stream, discipline, teacher, auditory)
                        self.schedule.add_event(event)
                    except Exception as e:
                        self.error_box.append(e)
            self.current_col += 2
        return len(self.error_box) == 0

    def __parse_stream(self, cell):
        if cell.value:
            return cell.value.strip()
        raise Exception('Ошибка в ячейки', cell.coordinate, cell.value)

    def __parse_discipline(self, cell):
        if '/' in cell.value and cell.value is not None:
            return cell.value.split('/')[0].strip()
        raise Exception('Ошибка в ячейки', cell.coordinate, cell.value)

    def __parse_teacher(self, cell):
        if '/' in cell.value and cell.value is not None:
            return cell.value.split('/')[1].strip()
        raise Exception('Ошибка в ячейки', cell.coordinate, cell.value)

    def __parse_auditory(self, cell):
        if cell.value:
            return str(cell.value).strip()
        raise Exception('Ошибка в ячейки', cell.coordinate, cell.value)

    def __check_data_db(self, department):
        """ Функция проверки наличия информации в базе данных """
        logger.info('Проверка расписания в базе данных')
        for group, couples in self.schedule.schedule.items():
            for couple, events in couples.items():
                for event in events:
                    try:
                        stdgrp = Studygroup.objects.get(department=department, name=group)
                        gs = GroupStream.objects.get(group=stdgrp)
                        couple = Couple.objects.get(number=couple, stream=gs.stream)
                        discipline = Discipline.objects.get(name=event.get('discipline'))
                        auditory = Auditory.objects.get(number=event.get('auditory'), department=department)
                        teacher = CustomPerson.objects.get(
                            last_name=re.split(r'[.\s]', event.get('teacher'))[0],
                            first_name__contains=re.split(r'[.\s]', event.get('teacher'))[1],
                            middle_name__contains=re.split(r'[.\s]', event.get('teacher'))[2],
                            is_teacher=True
                        )
                    except ObjectDoesNotExist as e:
                        self.error_box.append(f'{e} {event}')
                    except Exception as e:
                        self.error_box.append(e)
        return len(self.error_box) == 0

    def __save_change_gb(self, department: Department = None, date_range: list = None):
        logger.info('Добавление расписания в базу данных')
        model = Schedule
        for date in date_range:
            logger.info('Добавление расписания на %s' % date)
            for group, couples in self.schedule.schedule.items():
                for couple, events in couples.items():
                    for event in events:
                        stdgrp = Studygroup.objects.get(department=department, name=group)
                        gs = GroupStream.objects.get(group=stdgrp)
                        grp_couple = Couple.objects.get(number=couple, stream=gs.stream)
                        discipline = Discipline.objects.get(name=event.get('discipline'))
                        auditory = Auditory.objects.get(number=event.get('auditory'), department=department)
                        teacher = CustomPerson.objects.get(
                            last_name=re.split(r'[.\s]', event.get('teacher'))[0],
                            first_name__contains=re.split(r'[.\s]', event.get('teacher'))[1],
                            middle_name__contains=re.split(r'[.\s]', event.get('teacher'))[2],
                            is_teacher=True
                        )
                        e = model(
                            date=date,
                            couple=grp_couple,
                            group=stdgrp,
                            auditory=auditory,
                            discipline=discipline,
                            teacher=teacher
                        )
                        e.save()
                        logger.info(e)
        else:
            return True
