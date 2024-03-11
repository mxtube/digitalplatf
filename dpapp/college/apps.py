import os
from core.settings import MEDIA_ROOT
from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_media_folders(sender, **kwargs):
    for i in ['img', 'json', 'pix', 'video', 'xls']:
        if not os.path.exists(MEDIA_ROOT + i):
            os.makedirs(MEDIA_ROOT + i)


class CollegeConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'college'
    verbose_name = 'Колледж'

    def ready(self):
        post_migrate.connect(create_media_folders, sender=self)
