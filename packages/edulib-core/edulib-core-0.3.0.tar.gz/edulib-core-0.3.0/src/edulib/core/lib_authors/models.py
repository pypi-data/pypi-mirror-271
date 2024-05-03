"""Модели справочника Авторы."""
from django.core.exceptions import (
    ValidationError,
)
from django.db import (
    models,
)
from django.db.models import (
    CASCADE,
)

from edulib.core.base.models import (
    BaseModel,
)


class LibraryAuthors(BaseModel):
    """Справочник Авторы."""

    name = models.CharField('Автор', max_length=256, db_index=True, unique=True)

    def __str__(self):
        """Представление модели."""
        # pylint: disable=invalid-str-returned
        return self.name

    def safe_delete(self):
        """Безопасное удаление."""
        if self.__class__.objects.filter(
                libauthorsregentries__author=self).exists():
            raise ValidationError(
                f'Запись {self.name} не может быть удалена, т.к. у нее есть связи'
            )
        self.delete()
        return True

    class Meta:
        db_table = 'lib_authors'
        ordering = ['name', ]
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class LibAuthorsRegEntries(BaseModel):
    """Модель связи авторов и экземпляров библиотеки."""

    audit_log = True  # Включение логирования для этой модели

    author = models.ForeignKey(
        LibraryAuthors,
        verbose_name='Автор',
        on_delete=CASCADE,
    )
    reg_entry = models.ForeignKey(
        'lib_registry.LibRegistryEntry',
        verbose_name='Библиотечный экземпляр',
        on_delete=CASCADE,
    )

    class Meta:
        db_table = 'lib_authors_regentries'
        verbose_name = 'Автор экземпляра'
        verbose_name_plural = 'Авторы экземпляров'
