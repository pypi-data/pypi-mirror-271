# pylint: disable=import-outside-toplevel
from django.core.exceptions import (
    ValidationError,
)
from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)
from edulib.core.lib_example_types import (
    domain,
)
from edulib.core.lib_example_types.domain.model import (
    ReleaseMethod,
)


class LibraryExampleType(BaseModel):
    """Тип библиотечных экземпляров."""

    CLASSBOOK_ID = 1

    name = models.CharField(
        verbose_name=domain.ExampleType.name.title,
        max_length=domain.ExampleType.name.max_length,
        db_index=True,
    )
    release_method = models.PositiveSmallIntegerField(
        verbose_name=domain.ExampleType.release_method.title,
        choices=ReleaseMethod.choices(),
        default=ReleaseMethod.PRINTED,
    )

    def safe_delete(self):
        """Безопасное удаление экземпляра."""
        from edulib.core.lib_registry.models import (
            LibRegistryEntry,
        )
        if LibRegistryEntry.objects.filter(type=self).exists():
            raise ValidationError(
                'Невозможно удалить тип библиотечных экземпляров, '
                'так как в библиотечном реестре имеются карточки '
                'экземпляров этого типа!')
        self.delete()
        return True

    class Meta:
        db_table = 'lib_example_types'
        verbose_name = 'Тип библиотечных экземпляров'
