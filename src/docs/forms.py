from django import forms
from .models import Article
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ArticleAdminForm(forms.ModelForm):

    content = forms.CharField(label='Содержание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = '__all__'
