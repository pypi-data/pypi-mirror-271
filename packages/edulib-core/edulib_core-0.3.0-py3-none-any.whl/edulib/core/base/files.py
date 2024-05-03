import datetime
import os
import uuid

from django.utils.text import (
    get_valid_filename,
)

import edulib


def get_abspath(path):
    """
    :param path: путь (абсолютный или относительный)
    :type path: str
    :return: абсолютный путь
    :rtype: str
    """
    if os.path.isabs(path):
        return path
    return os.path.join(os.getcwd(), path)


def get_valid_file_name_and_extension(filename, as_uid):
    """Возвращает валидное расширение и название файла."""

    file_name, file_extension = (filename.rsplit('.', 1) + [''])[:2]

    file_extension = get_valid_filename(file_extension) or 'dat'
    uid = uuid.uuid4().hex

    if as_uid:
        new_filename = uid
    else:
        new_filename = get_valid_filename(file_name) or uid
    return file_extension, new_filename


def get_upload_file_path(prefix, filename, as_uid=True, func=None):
    """Получение пути для upload.

    :param prefix: инстанс модели, которая содержит поле с файлом
        (используется в т.ч. для формирования подпути)
    :type: str
    :param filename: исходное имя файла
    :type: str
    :param func: Функция, которая принимает расширение файла и
        вовзращает название для файла
    :rtype: str
    :return путь вида '/uploads/Название модели/год/месяц/день/knfkfiywuq9.jpg'
    """
    if callable(func):
        file_extension = filename.split('.')[-1]
        new_filename = func(file_extension)
    else:
        file_extension, new_filename = get_valid_file_name_and_extension(
            filename, as_uid)
        new_filename = new_filename[:32] + '.' + file_extension

    date = datetime.datetime.now()

    return os.path.join(
        edulib.get_config().uploads_dir,
        prefix,
        date.strftime('%Y/%m/%d'),
        new_filename
    )


def upload_file_handler(instance, filename, as_uid=True, func=None):
    """Вызывается при загрузке файла.

    Генерирует иерархический путь
    :param instance: инстанс модели, которая содержит поле с файлом
        (используется в т.ч. для формирования подпути)
    :param unicode filename: исходное имя файла
    :param func: Функция, которая принимает расширение файла и
        вовзращает название для файла

    :return str: '/uploads/Название модели/год/месяц/день/knflakfiywuq9.jpg'
    """
    return get_upload_file_path(
        instance.__class__.__name__.lower(),
        filename,
        as_uid=as_uid,
        func=func)


def upload_named_handler(instance, filename):
    return upload_file_handler(instance, filename, as_uid=False)
