import datetime
from django import forms
from college.models import Department, CustomPerson
from .models import DayWeek


class UploadBaseScheduleForm(forms.Form):

    file = forms.FileField(label='Файл')
    date = forms.ModelChoiceField(label='День недели', queryset=DayWeek.objects.all())
    department = forms.ModelChoiceField(label='Площадка', queryset=Department.objects.all())


class UploadChangeScheduleForm(forms.Form):

    file = forms.FileField(label='Файл')
    date = forms.DateField(label='Дата', initial=datetime.date.today())
    department = forms.ModelChoiceField(label='Площадка', queryset=Department.objects.all())


class ScheduleDateForm(forms.Form):

    date = forms.DateField(label='Дата', widget=forms.NumberInput(attrs={'type': 'date'}))


class ScheduleTeacherForm(forms.Form):
    # TODO: Список преподавателей по расписанию на выбранный день
    teacher = forms.ModelChoiceField(CustomPerson.objects.all(), label='ФИО преподавателя')