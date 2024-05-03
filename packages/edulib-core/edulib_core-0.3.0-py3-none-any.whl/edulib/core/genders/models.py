from django.db import (
    models,
)

from edulib.core.base.models import (
    SimpleDictionary,
)
from edulib.core.genders import (
    domain,
)


class Gender(SimpleDictionary):
    """Проекция "Пол"."""

    external_id = models.CharField(
        verbose_name=domain.Gender.external_id.title,
        max_length=domain.Gender.external_id.max_length,
        db_index=True,
    )

    class Meta:
        db_table = 'gender'
        verbose_name = 'Пол'
        verbose_name_plural = 'Полы'
