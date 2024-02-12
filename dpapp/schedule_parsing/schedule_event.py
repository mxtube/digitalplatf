"""
Copyright (c) 2022-2024 schedule parsing
Development @KirillKuznetsov
Schedule Item 10.02.2024
"""


class ScheduleEvent:

    def __init__(self, group: str, couple: str, auditory: str, discipline: str, teacher: str):
        self.group = group
        self.couple = couple
        self.auditory = auditory
        self.discipline = discipline
        self.teacher = teacher

    def __str__(self):
        return f'{self.group} {self.couple} {self.auditory} {self.discipline} {self.teacher}'
