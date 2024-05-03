from django.db import (
    models,
)

from edulib.core.base.models import (
    SimpleDictionary,
)
from edulib.core.institution_types import (
    domain,
)


class InstitutionType(SimpleDictionary):
    """Проекция "Тип организации"."""

    external_id = models.CharField(
        verbose_name=domain.InstitutionType.external_id.title,
        max_length=domain.InstitutionType.external_id.max_length,
        db_index=True,
    )

    class Meta:
        db_table = 'institution_type'
        verbose_name = 'Тип организации'
        verbose_name_plural = 'Типы организациий'
