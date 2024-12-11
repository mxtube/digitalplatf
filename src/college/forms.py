from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError

from .models import SiteSettings, CustomPerson


class SiteSettingsAdminForm(forms.ModelForm):

    description = forms.CharField(widget=CKEditorUploadingWidget(), label="Описание главной страницы")

    class Meta:
        model = SiteSettings
        fields = '__all__'


class CustomPasswordResetForm(PasswordResetForm):
    # https://docs.djangoproject.com/en/5.1/topics/auth/default/#django.contrib.auth.forms.PasswordResetForm
    """
    Форма восстановления пароля по электронной почте
    """
    corp_email = forms.EmailField(label="КП11 ID", max_length=100, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'ivanov@corp.kp11.ru', 'autocomplete': 'email'
    }))
    email = forms.EmailField(label="Личная почта", max_length=150, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'ivanov@yandex.ru', 'autocomplete': 'email'
    }))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        corp_email = cleaned_data.get('corp_email')

        if not email or not corp_email:
            raise ValidationError("Оба поля обязательны для заполнения")

        try:
            user = CustomPerson.objects.get(email=email, username=corp_email)
        except CustomPerson.DoesNotExist:
            raise ValidationError("Пользователь с такими данными не найден")

        self.cleaned_data['user'] = user
        return cleaned_data


class SuggestionForm(forms.Form):
    """
    Форма обратной связи для идей и предложений
    Элементы:
    user (String) - поле идентификации пользователя по логину
    theme (String) - поле для ввода темы обращения
    message (String) - поле для ввода текста обращения
    """
    user = forms.CharField(label='КП ID', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    theme = forms.CharField(label='Тема', min_length=10, max_length=150,
                            widget=forms.TextInput(attrs={'placeholder': 'Напишите тему вашего обращения'}))
    message = forms.CharField(label='Сообщение', min_length=10, max_length=5000,
                              widget=forms.Textarea(attrs={'placeholder': 'Напишите тут ваше сообщение', 'rows': '8'}))


class EditProfileForm(forms.ModelForm):

    mobile = forms.CharField(label='Мобильный телефон', required=False,
                             help_text='Номер телефона в формате +79998887766')
    alternative_email = forms.EmailField(label='Личный адрес электронной почты', required=True)

    class Meta:
        model = CustomPerson
        fields = ['mobile', 'alternative_email']
