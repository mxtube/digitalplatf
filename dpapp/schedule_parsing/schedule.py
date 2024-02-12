"""
Copyright (c) 2022-2024 schedule parsing
Development @KirillKuznetsov
Schedule 10.02.2024
"""
from datetime import date


class Schedule:

    def __init__(self, from_date: date, department: str):
        self.date = from_date
        self.department = department
        self.schedule_data: list = []

    def __str__(self):
        return f'{self.date}, {self.department}'

    def add_event(self, event):
        return self.schedule_data.append(event.__dict__)

    def display_group(self, name: str):
        return list(
            filter(lambda group: group['group'] == name, self.schedule_data)
        )

    def display_schedule(self):
        """
        Function returned schedule by date and department
        :return:
        """
        return [{"date": self.date.__str__(), "department": self.department, "data": self.schedule_data}]
