import datetime
from django import forms
from college.models import Department, CustomPerson
from .models import DayWeek, ChangeSchedule


class DepartmentForm(forms.Form):

    department = forms.ModelChoiceField(label='Площадка', queryset=Department.objects.all())


class UploadBaseScheduleFormAdmin(forms.Form):

    file = forms.FileField(label='Файл')
    date = forms.ModelChoiceField(label='День недели', queryset=DayWeek.objects.all())
    department = forms.ModelChoiceField(label='Площадка', queryset=Department.objects.all())


class UploadChangeScheduleFormAdmin(forms.Form):

    file = forms.FileField(label='Файл')
    date = forms.DateField(label='Дата', initial=datetime.date.today())
    department = forms.ModelChoiceField(label='Площадка', queryset=Department.objects.all())

    def clean_date(self):
        date = self.cleaned_data['date']
        if ChangeSchedule.has_schedule_by_date(date):
            self.add_error('date', 'Указанная дата в расписании уже существует')
        return date


class ScheduleDateForm(forms.Form):

    date = forms.DateField(label='Дата', widget=forms.NumberInput(attrs={'type': 'date'}))


class ScheduleTeacherForm(forms.Form):
    # TODO: Список преподавателей по расписанию на выбранный день
    teacher = forms.ModelChoiceField(CustomPerson.objects.all(), label='ФИО преподавателя')