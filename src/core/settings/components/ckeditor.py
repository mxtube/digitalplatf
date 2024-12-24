# CKEditor
# https://django-ckeditor.readthedocs.io/en/latest/#installation

# TODO: изменить путь сохранения файлов для разных типов
CKEDITOR_UPLOAD_PATH = 'ckeditor/'

# TODO: Скрываем предупреждение о CKEditor 4.22.1, проверить обновление в будущем
SILENCED_SYSTEM_CHECKS = ['ckeditor.W001']
