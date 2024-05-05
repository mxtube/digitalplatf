from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import SiteSettings


class SiteSettingsAdminForm(forms.ModelForm):

    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = SiteSettings
        fields = '__all__'