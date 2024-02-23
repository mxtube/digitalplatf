from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SiteSettings, CustomPerson, Department, Auditory
from .forms import SiteSettingsAdminForm


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):

    form = SiteSettingsAdminForm

    fieldsets = (
        ('Общая информация', {
            'fields': (('site_name', 'short_site_name', 'logotype', 'description',)),
            'description': '',
        }),
        ('Контактная информация', {
            'fields': (('contact_description'), ('phone', 'email', 'address',),),
            'classes': ('wide',),
        }),
        ('Социальные сети', {
            'description': 'Ссылки на социальные сети, отображаемые на страницах сайта.',
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


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = ('name', 'short_name', 'supervisor', 'coordinate', 'phone')
    list_display_links = list_display

    fieldsets = (
        ('Общая информация', {'fields': ('name', 'short_name'), }),
        ('Контакты', {'fields': ('phone', 'coordinate', 'supervisor'), }),
    )


@admin.register(Auditory)
class AuditoryAdmin(admin.ModelAdmin):

    list_display = ('number', 'department', )
    list_filter = ['department__name']