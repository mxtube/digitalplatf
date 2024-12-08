from django import forms
from .models import Type


class ReferenceChooseForm(forms.Form):
    """ Форма выбора справки """
    type = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        label='Выберите справку',
        empty_label='Выберите справку',
        widget=forms.Select(attrs={"class": "form-control"})
    )


class ReferenceMilitaryForm(forms.Form):
    """ Форма справки в военкомат """
    type = forms.CharField(label='Тип справки', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    student = forms.CharField(label='ФИО обучающегося', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    comment = forms.CharField(max_length=500, label='Наименование военкомата', widget=forms.TextInput(
        attrs={'placeholder': 'Военный комиссариат Бабушкинского района СВАО города Москвы'}
    ))
    count = forms.IntegerField(max_value=10, min_value=1, initial=1, label='Количество')


class ReferenceGrandForm(forms.Form):
    """ Форма справки выплат стипендии """
    type = forms.CharField(label='Тип справки', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    student = forms.CharField(label='ФИО обучающегося', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    comment = forms.CharField(max_length=500, label='Период', widget=forms.TextInput(attrs={'placeholder': 'Период'}))
    count = forms.IntegerField(max_value=10, min_value=1, initial=1, label='Количество')


class ReferenceEducationForm(forms.Form):
    """ Форма справки об обучении """
    type = forms.CharField(label='Тип справки', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    student = forms.CharField(label='ФИО обучающегося', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    count = forms.IntegerField(max_value=10, min_value=1, initial=1, label='Количество')


class ReferenceDiplomaForm(forms.Form):
    """ Форма получения копии документа об образовании """
    type = forms.CharField(label='Тип справки', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    student = forms.CharField(label='ФИО обучающегося', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    count = forms.IntegerField(max_value=10, min_value=1, initial=1, label='Количество')
