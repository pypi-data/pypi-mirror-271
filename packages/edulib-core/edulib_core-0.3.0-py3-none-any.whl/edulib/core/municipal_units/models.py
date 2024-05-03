from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)

from . import (
    domain,
)


class MunicipalUnit(BaseModel):
    """Проекция "Муниципальная единица"."""

    external_id = models.BigIntegerField(
        verbose_name=domain.MunicipalUnit.external_id.title,
        db_index=True,
    )
    code = models.CharField(
        verbose_name=domain.MunicipalUnit.code.title,
        max_length=domain.MunicipalUnit.code.max_length,
    )
    name = models.TextField(
        verbose_name=domain.MunicipalUnit.name.title,
        null=True
    )
    parent = models.ForeignKey(
        'self',
        verbose_name=domain.MunicipalUnit.parent.title,
        null=True,
        on_delete=models.PROTECT
    )
    constituent_entity = models.CharField(
        verbose_name=domain.MunicipalUnit.constituent_entity.title,
        max_length=domain.MunicipalUnit.constituent_entity.max_length,
    )
    okato = models.CharField(
        verbose_name=domain.MunicipalUnit.okato.title,
        max_length=domain.MunicipalUnit.okato.max_length,
        null=True
    )
    oktmo = models.CharField(
        verbose_name=domain.MunicipalUnit.oktmo.title,
        max_length=domain.MunicipalUnit.oktmo.max_length,
        null=True

    )

    class Meta:
        db_table = 'municipal_unit'
        verbose_name = 'Муниципальная единица'
        verbose_name_plural = 'Муниципальные единицы'
