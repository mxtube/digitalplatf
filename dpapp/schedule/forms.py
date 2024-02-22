from django import forms
from college.models import Department
from .models import DayWeek


class UploadBaseScheduleForm(forms.Form):

    file = forms.FileField(label='Файл')
    date = forms.ModelChoiceField(label='День недели', queryset=DayWeek.objects.all())
    department = forms.ModelChoiceField(label='Площадка', queryset=Department.objects.all())
