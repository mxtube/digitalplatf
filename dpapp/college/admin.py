from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SiteSettings, CustomPerson


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


@admin.register(CustomPerson)
class CustomUserAdmin(UserAdmin):

    model = CustomPerson

    add_fieldsets = (*UserAdmin.add_fieldsets, ('Дополнительная информация', {
        'fields': ('middle_name', 'mobile', 'birthday', 'note', 'alternative_email',
    )}))

    fieldsets = (*UserAdmin.fieldsets, ('Дополнительная информация', {
        'fields': ('middle_name', 'mobile', 'birthday', 'note', 'alternative_email',)}
    ))

    list_display = ('get_fullname', 'username', 'email', 'last_login', 'is_active',)
    list_display_links = ('get_fullname', 'username', 'email',)