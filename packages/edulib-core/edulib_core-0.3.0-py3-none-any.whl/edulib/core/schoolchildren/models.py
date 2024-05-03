from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)

from . import (
    domain,
)


class Schoolchild(BaseModel):

    class Meta:
        verbose_name = 'Учащийся школы'
        verbose_name = 'Учащиеся школ'
        db_table = 'schoolchild'

    person_id = models.BigIntegerField(
        verbose_name=domain.Schoolchild.person_id.title,
        unique=True, db_index=True
    )
