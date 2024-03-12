import os
from core.settings import MEDIA_ROOT
from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CollegeConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'college'
    verbose_name = 'Колледж'

    root_folders = ['img', 'json', 'pix', 'video', 'xls']
    user_folders = ['img/userpic']

    def ready(self):
        post_migrate.connect(self.create_media_folders, sender=self)

    def create_media_folders(self, sender, **kwargs):
        for i in self.root_folders + self.user_folders:
            if not os.path.exists(MEDIA_ROOT + i):
                os.makedirs(MEDIA_ROOT + i)
