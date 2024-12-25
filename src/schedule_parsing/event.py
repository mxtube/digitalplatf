"""
Created on Thu 7.03.24
@author: Kirill Kuznetsov
"""


class Event:
    def __init__(
            self,
            group: str,
            couple: str,
            discipline: str,
            teacher: str,
            auditory: str
    ):
        self.group = group
        self.couple = couple
        self.discipline = discipline
        self.teacher = teacher
        self.auditory = auditory

    def __str__(self):
        return f'{self.couple} {self.discipline} {self.teacher} {self.auditory}'

    @property
    def group(self):
        return f'{self._group}'

    @group.setter
    def group(self, value):
        self._group = value.strip()

    @property
    def couple(self):
        return f'{self._couple}'

    @couple.setter
    def couple(self, value):
        self._couple = value.strip()

    @property
    def discipline(self):
        return f'{self._discipline}'

    @discipline.setter
    def discipline(self, value):
        self._discipline = value.strip()

    @property
    def teacher(self):
        return f'{self._teacher}'

    @teacher.setter
    def teacher(self, value):
        clean_name = value.split()
        if len(clean_name) not in (2, 3):
            raise ValueError(f'Ошибка в имени преподавателя. Ожидается 2 или 3 слова, но получено {len(clean_name)}.')
        self._teacher = value.strip()

    @property
    def auditory(self):
        return f'{self._auditory}'


    @auditory.setter
    def auditory(self, value):
        self._auditory = value.strip()
