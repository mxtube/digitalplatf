import datetime
from django import forms
from college.models import Department, CustomPerson
from .models import Schedule, DayWeek
from django.core.exceptions import ValidationError


class DepartmentForm(forms.Form):

    department = forms.ModelChoiceField(label='Площадка', queryset=Department.objects.all())


class UploadSchedulesFormAdmin(forms.Form):

    file = forms.FileField(label='Файл')
    day = forms.ModelChoiceField(DayWeek.objects.all(), label='День недели', widget=forms.Select(attrs={"class": "form-control"}))
    start_date = forms.DateField(
        label='С',
        initial=datetime.date.today(),
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )
    end_date = forms.DateField(
        label='По',
        initial=datetime.date.today(),
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )
    start_row = forms.IntegerField(label='Начало строки', initial=2)
    department = forms.ModelChoiceField(label='Площадка', queryset=Department.objects.all())

    def clean(self):
        """ Проверяем что на выбранные даты нет расписания """
        cleaned_data = super().clean()
        start = datetime.date.strftime(cleaned_data.get('start_date'), '%Y-%m-%d')
        end = datetime.date.strftime(cleaned_data.get('end_date'), '%Y-%m-%d')
        day = cleaned_data.get('day').__str__()
        if start and end and day:
            if Schedule.has_date_by_range(start, end, day):
                raise ValidationError('В выбранном диапазоне существует расписание')


class ScheduleDateForm(forms.Form):

    date = forms.DateField(label='Дата', widget=forms.NumberInput(attrs={'type': 'date'}))


class ScheduleTeacherForm(forms.Form):

    teacher = forms.ModelChoiceField(Schedule.objects.all(), label='ФИО преподавателя')


