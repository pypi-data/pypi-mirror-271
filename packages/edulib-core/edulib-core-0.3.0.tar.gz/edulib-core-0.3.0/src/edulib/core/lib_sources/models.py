# pylint: disable=invalid-str-returned
from django.db import (
    models,
)
from django.forms import (
    ValidationError,
)

from edulib.core.base.models import (
    BaseModel,
)


class LibrarySource(BaseModel):

    """Источник поступления книг в библиотеку"""

    name = models.TextField(
        verbose_name='Источник поступления',
    )
    school_id = models.BigIntegerField(
        verbose_name='Организация',
    )

    def safe_delete(self):
        if self.libregistryentry_set.exists():
            raise ValidationError(
                f'Запись "{self.name}" не может быть удалена, т.к. у нее есть связи'
            )
        self.delete()
        return True

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'library_source'
        ordering = ('name',)
        verbose_name = 'Источник поступления'
        verbose_name_plural = 'Источники поступления'
