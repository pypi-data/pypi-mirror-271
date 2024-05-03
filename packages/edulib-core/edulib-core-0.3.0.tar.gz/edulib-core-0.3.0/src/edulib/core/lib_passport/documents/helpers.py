from django.core.exceptions import (
    ValidationError,
)
from django.template.defaultfilters import (
    filesizeformat,
)

import edulib
from edulib.core.lib_passport.documents.models import (
    LibPassportDocuments,
)


def get_documents_by_type(obj, type_):
    """
    Получение документов паспорта библиотеки по типу
    """
    query = LibPassportDocuments.objects.none()
    if obj:
        if type_ == 'legal':
            query = obj.documents_legal.all()
        elif type_ == 'account':
            query = obj.documents_account.all()

    return query


def check_max_filesize(filesize):
    """
    Функция проверки размера файла на превышение максимального размера,
    указанного в settings
    """
    config = edulib.get_config()
    if filesize > int(config.max_upload_size):
        raise ValidationError(
            f'Размер файла должен быть меньше {filesizeformat(config.MAX_UPLOAD_SIZE)}. '
            f'Текущий размер файла {filesizeformat(filesize)}'
        )
