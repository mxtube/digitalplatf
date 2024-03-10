from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SiteSettings, CustomPerson, Department, Auditory, UserServicesCategory, UserServices
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

    list_display = ('get_fullname', 'username', 'email', 'last_login', 'is_active',)
    list_display_links = ('get_fullname', 'username', 'email',)
    ordering = ('-last_login',)
    search_fields = ['username', 'email', 'first_name', 'last_name', 'middle_name']
    autocomplete_fields = ['group']
    add_fieldsets = (
        *UserAdmin.fieldsets,
        ('Дополнительная информация', {'fields': ('middle_name', 'alternative_email',)})
    )

    fieldsets = (
        (None, {'fields': ('username', 'email',),}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'middle_name', 'mobile', 'alternative_email',),}),
        ('Дополнительная информация', {'fields': ('group', 'note',),}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_teacher', 'groups', 'user_permissions',),}),
        ('Статус', {'fields': ('last_login', 'date_joined'),}),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = ('name', 'short_name', 'supervisor', 'coordinate', 'phone')
    list_display_links = list_display
    prepopulated_fields = {"slug": ("short_name",)}
    autocomplete_fields = ['supervisor']

    fieldsets = (
        ('Общая информация', {'fields': ('name', 'short_name', 'slug',), }),
        ('Контакты', {'fields': ('phone', 'coordinate', 'supervisor'), }),
    )


@admin.register(Auditory)
class AuditoryAdmin(admin.ModelAdmin):

    list_display = ('number', 'department', )
    list_filter = ['department__name']


@admin.register(UserServicesCategory)
class UserServicesCategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'visible',)
    list_display_links = list_display


@admin.register(UserServices)
class UserServicesAdmin(admin.ModelAdmin):

    list_display = ('category', 'name', 'link', 'icon', 'visible',)
    list_display_links = list_display