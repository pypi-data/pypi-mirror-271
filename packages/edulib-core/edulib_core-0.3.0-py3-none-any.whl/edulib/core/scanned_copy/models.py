from django.db.models import (
    CharField,
    FileField,
)
from django.db.models.fields import (
    BigIntegerField,
)

from edulib.core.base.files import (
    upload_named_handler,
)
from edulib.core.base.models import (
    BaseModel,
)


class ScannedCopy(BaseModel):

    """Скан-копия."""

    audit_log = True
    school_id = BigIntegerField(
        verbose_name='Школа', null=True, blank=True
    )
    name = CharField(max_length=256, verbose_name='Наименование')
    filename = FileField(
        upload_to=upload_named_handler,
        max_length=255,
        verbose_name='Файл'
    )

    class Meta:
        db_table = 'library_scanned_copy'
        verbose_name = 'Скан-копия'
        verbose_name_plural = 'Скан-копии'
