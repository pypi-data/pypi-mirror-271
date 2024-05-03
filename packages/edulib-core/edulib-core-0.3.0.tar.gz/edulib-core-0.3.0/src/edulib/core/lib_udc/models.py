# pylint: disable=invalid-str-returned, import-outside-toplevel
from django.core.exceptions import (
    ValidationError as DjangoValidationError,
)
from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)


class LibraryUDC(BaseModel):
    """Раздел УДК"""
    audit_log = True  # Включение логирования для этой модели

    code = models.CharField('Код', max_length=32, db_index=True)
    name = models.CharField(
        'Наименование', max_length=900, null=True, blank=True, db_index=True)
    index_udc = models.CharField(
        'Индекс', max_length=10, null=True, blank=True, db_index=True, )

    def display(self):
        return self.index_udc
    display.json_encode = True

    def __str__(self):
        """Юникодное представление модели."""
        return self.index_udc

    def save(self, *args, **kwargs):
        self.code = (self.code or '').strip()
        self.name = (self.name or '').strip()

        if not self.name:
            raise DjangoValidationError(
                'Наименование не может быть пустым!')

        current_objs = self.__class__.objects.exclude(id=self.id)

        if current_objs.filter(code__iexact=self.code).exists():
            raise DjangoValidationError(
                'Объект с данным кодом уже существует!')

        super().save(*args, **kwargs)

    def safe_delete(self):
        # TODO: Циклический импорт.
        # TODO: Выделить метод .get_by_udc(udc) в репозитории
        # TODO: Перенести бизнес-логику из модели в обработчик сервисного слоя
        from edulib.core.lib_registry.models import (
            LibRegistryEntry,
        )
        if LibRegistryEntry.objects.filter(udc=self).exists():
            raise DjangoValidationError(
                'Невозможно удалить раздел УДК, так как в библиотечном реестре '
                'имеются карточки экземпляров этого раздела!')
        self.delete()
        return True

    class Meta:
        db_table = 'lib_udc'
        verbose_name = 'Раздел УДК'
        verbose_name_plural = 'Разделы УДК'
