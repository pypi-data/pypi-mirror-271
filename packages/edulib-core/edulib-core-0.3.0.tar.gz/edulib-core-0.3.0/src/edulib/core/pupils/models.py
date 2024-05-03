from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)

from . import (
    domain,
)


class Pupil(BaseModel):

    """Проекция "Учащийся" (образование ФЛ)."""

    class Meta:
        db_table = 'pupil'
        verbose_name = 'Учащийся'
        verbose_name_plural = 'Учащиеся'

    external_id = models.CharField(
        verbose_name=domain.Pupil.external_id.title,
        max_length=domain.Pupil.external_id.max_length,
        db_index=True,
    )
    training_begin_date = models.DateField(
        verbose_name=domain.Pupil.training_begin_date.title,
    )
    training_end_date = models.DateField(
        verbose_name=domain.Pupil.training_end_date.title,
        null=True, blank=True
    )
    schoolchild_id = models.BigIntegerField(
        verbose_name=domain.Pupil.schoolchild_id.title,
    )
    class_year_id = models.BigIntegerField(
        verbose_name=domain.Pupil.class_year_id.title,
    )
    school_id = models.BigIntegerField(
        verbose_name=domain.Pupil.school_id.title,
    )
