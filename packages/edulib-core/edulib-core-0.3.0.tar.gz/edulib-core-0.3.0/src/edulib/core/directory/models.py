# pylint: disable=invalid-str-returned
import mptt
from django.apps import (
    apps,
)
from django.db import (
    models,
)
from django.db.transaction import (
    atomic,
)

from edulib.core.base.models import (
    BaseModel,
)
from edulib.core.directory import (
    domain,
)


class Catalog(BaseModel):
    """Библиотечно-библиографическая классификация."""

    code = models.CharField(
        verbose_name=domain.Bbk.code.title,
        max_length=domain.Bbk.code.max_length,
        db_index=True,
    )
    name = models.CharField(
        verbose_name=domain.Bbk.name.title,
        max_length=domain.Bbk.name.max_length,
        db_index=True,
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'library_catalog'
        verbose_name = 'Библиотечно-библиографическая классификация'
        verbose_name_plural = 'Библиотечно-библиографическая классификация'

    def display(self):
        return self.code
    display.json_encode = True

    def __str__(self):
        return self.code

    @atomic
    def save(self, *args, **kwargs):
        """Удаление записей в моделях кол-ва документов по ББК в КСУ."""
        super().save(*args, **kwargs)
        # Если текущая запись не корневая, то связанные записи
        # в моделях кол-ва документов по ББК в КСУ следует удалить:
        if self.parent:
            self.clean_related()

    def clean_related(self):
        """Удаляет объекты связей с книгой учёта.

            Объекты создаются асинхронным таском.
        """
        apps.get_model(
            'lib_registry', 'LibSummaryBookCatalog'
        ).objects.filter(bbc=self).delete()
        apps.get_model(
            'lib_registry', 'LibSummaryBookDisposalCatalog'
        ).objects.filter(bbc=self).delete()


mptt.register(Catalog, order_insertion_by=['name'])
