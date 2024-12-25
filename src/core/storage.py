import os


def get_media_upload_path(instance, filename):
    """
    Возвращает путь для сохранения файла в зависимости от расширения.
    Все изображения -> media/img/
    Все видео -> media/video/
    Остальные файлы -> media/files/
    """
    # Получаем расширение файла в нижнем регистре
    ext = os.path.splitext(filename)[1].lower()

    # Список (или кортеж) расширений для изображений
    IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp']
    # Список расширений для видео
    VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv']

    # Определяем папку сохранения
    if ext in IMAGE_EXTENSIONS:
        folder = 'img'
    elif ext in VIDEO_EXTENSIONS:
        folder = 'video'
    else:
        folder = 'files'

    return os.path.join(folder, filename)
