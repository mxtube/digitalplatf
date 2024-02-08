from django.contrib import admin
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Общая информация', {
            'fields': (('site_name', 'logotype',)),
            'description': '',
        }),
        ('Контактная информация', {
            'fields': (('contact_description'), ('phone', 'email', 'address',),),
            'classes': ('wide',),
        }),
        ('Социальные сети', {
            'fields': ('vk_link', 'youtube_link', 'odnoklassniki_link', 'dzen_link', 'telegram_link', 'whatsapp_link',),
        }),
    )

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        try:
            SiteSettings.load().save()
        except Exception as e:
            pass

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
