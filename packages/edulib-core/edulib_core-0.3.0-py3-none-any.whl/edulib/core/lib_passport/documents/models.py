from django.db import (
    models,
)

from edulib.core.base.domain import (
    BaseEnumerate,
)
from edulib.core.base.files import (
    upload_file_handler,
)
from edulib.core.base.models import (
    BaseModel,
)


class DocumentTypeEnum(BaseEnumerate):
    """
    Тип документа
    """

    LEGAL, ACCOUNT = 1, 2
    values = {
        LEGAL: 'Норативно-правовая база',
        ACCOUNT: 'Документы учета работы библиотеки',
    }


class LibPassportDocuments(BaseModel):
    audit_log = True

    doc_type = models.PositiveIntegerField(
        'Тип документа',
        choices=DocumentTypeEnum.get_choices(),
        null=True, blank=True
    )
    name = models.CharField(max_length=200, verbose_name='Наименование')
    document = models.FileField(
        upload_to=upload_file_handler,
        max_length=255, verbose_name='Файл',
        blank=True, null=True
    )

    class Meta:
        db_table = 'library_passport_documents'
        verbose_name = 'Документы библиотеки'
        verbose_name_plural = 'Документы библиотеки'
