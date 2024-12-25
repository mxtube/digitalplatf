import os
import pytest
from unittest.mock import Mock
from core.storage import get_media_upload_path


@pytest.mark.parametrize("filename,expected_folder", [
    ("photo.jpg", "img"), ("photo.1.jpg", "img"), ("photo-1.jpg", "img"), ("photo_1.jpg", "img"),
    ("picture.jpeg", "img"), ("1.picture.jpeg", "img"), ("1-picture.jpeg", "img"), ("_picture.jpeg", "img"),
    ("image.png", "img"), ("ima.ge.png", "img"), ("im-age.png", "img"), ("im_age.png", "img"),
    ("movie.mp4", "video"), ("mo.vie.mp4", "video"), ("mov-ie.mp4", "video"), ("mov_ie.mp4", "video"),
    ("clip.mkv", "video"), ("1.clip.mkv", "video"), ("1-clip.mkv", "video"), ("1_clip.mkv", "video"),
    ("document.pdf", "files"), ("document.1.pdf", "files"), ("document-1.pdf", "files"), ("document_.pdf", "files"),
    ("spreadsheet.xls", "files"), ("spre.adsheet.xls", "files"), ("spreads-heet.xls", "files"),
    ("archive.zip", "files"), (".archive.zip", "files"), ("arch-ive.zip", "files"), ("_archive.zip", "files"),
])
def test_get_media_upload_path(filename, expected_folder):
    """
    Проверяем, что функция get_media_upload_path корректно определяет папку
    в зависимости от расширения файла.
    """
    mock_instance = Mock()  # Модель нам не важна, поэтому используем заглушку
    path = get_media_upload_path(mock_instance, filename)

    # Проверяем, что путь начинается с нужной папки
    # path, например, может получиться: "img/photo.jpg"
    splitted = path.split(os.path.sep)
    # splitted[0] == "img" или "video" или "files"
    folder_part = splitted[0]
    filename_part = splitted[1]

    assert folder_part == expected_folder, (
        f"Для файла {filename} ожидаем папку '{expected_folder}', "
        f"но получили '{folder_part}'."
    )
    assert filename_part == filename, (
        f"Имена файлов не совпадают: ожидали '{filename}', а получили '{filename_part}'."
    )
