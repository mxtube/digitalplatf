"""
Created on Thu 7.03.24
@author: Kirill Kuznetsov
"""


class Event:
    def __init__(self, group, couple, discipline, teacher, auditory):
        self.group = group
        self.couple = couple
        self.discipline = discipline
        self.teacher = teacher
        self.auditory = auditory

    def __str__(self):
        return f"{self.couple} {self.discipline} {self.teacher} {self.auditory}"
