from django.db import (
    models,
)

from edulib.core.academic_years import (
    domain,
)
from edulib.core.base.models import (
    SimpleDictionary,
)


class AcademicYear(SimpleDictionary):

    """Проекция "Учебный год"."""

    external_id = models.CharField(
        verbose_name=domain.AcademicYear.external_id.title,
        max_length=domain.AcademicYear.external_id.max_length,
        db_index=True,
    )
    date_begin = models.DateField(verbose_name=domain.AcademicYear.date_begin.title)
    date_end = models.DateField(verbose_name=domain.AcademicYear.date_end.title)

    class Meta:
        db_table = 'academic_year'
        verbose_name = 'Учебный год'
        verbose_name_plural = 'Учебные годы'
