from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import SiteSettings


class SiteSettingsAdminForm(forms.ModelForm):

    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = SiteSettings
        fields = '__all__'

class SuggestionForm(forms.Form):
    """
    Форма обратной связи для идей и предложений
    Элементы:
    user (String) - поле идентификации пользователя по логину
    theme (String) - поле для ввода темы обращения
    message (String) - поле для ввода текста обращения
    """
    user = forms.CharField(label='КП ID', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    theme = forms.CharField(label='Тема', min_length=10, max_length=150,
                            widget=forms.TextInput(attrs={'placeholder': 'Напишите тему вашего обращения'}))
    message = forms.CharField(label='Сообщение', min_length=10, max_length=5000,
                              widget=forms.Textarea(attrs={'placeholder': 'Напишите тут ваше сообщение', 'rows': '8' }))