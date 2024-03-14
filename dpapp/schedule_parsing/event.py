"""
Created on Thu 7.03.24
@author: Kirill Kuznetsov
"""


class Event:
    def __init__(self, group, couple, discipline, teacher, auditory):
        self._group = group
        self._couple = couple
        self._discipline = discipline
        self._teacher = teacher
        self._auditory = auditory

    def __str__(self):
        return f"{self._couple} {self._discipline} {self._teacher} {self._auditory}"
