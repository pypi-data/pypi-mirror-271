from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)

from . import (
    domain,
)


class School(BaseModel):
    """Проекция "Организация"."""

    external_id = models.BigIntegerField(
        verbose_name=domain.School.external_id.title,
        db_index=True,
    )
    short_name = models.CharField(
        verbose_name=domain.School.short_name.title,
        max_length=domain.School.short_name.max_length,
    )
    name = models.TextField(
        verbose_name=domain.School.name.title,
        null=True
    )
    inn = models.CharField(
        verbose_name=domain.School.inn.title,
        max_length=domain.School.inn.max_length,
        null=True
    )
    kpp = models.CharField(
        verbose_name=domain.School.kpp.title,
        max_length=domain.School.kpp.max_length,
        null=True
    )
    okato = models.CharField(
        verbose_name=domain.School.okato.title,
        max_length=domain.School.okato.max_length,
        null=True
    )
    oktmo = models.CharField(
        verbose_name=domain.School.oktmo.title,
        max_length=domain.School.oktmo.max_length,
        null=True
    )
    oktmo = models.CharField(
        verbose_name=domain.School.oktmo.title,
        max_length=domain.School.oktmo.max_length,
        null=True
    )
    okpo = models.CharField(
        verbose_name=domain.School.okpo.title,
        max_length=domain.School.okpo.max_length,
        null=True
    )
    ogrn = models.CharField(
        verbose_name=domain.School.ogrn.title,
        max_length=domain.School.ogrn.max_length,
        null=True
    )
    institution_type_id = models.BigIntegerField(
        verbose_name=domain.School.institution_type_id.title,
        null=True
    )
    f_address_id = models.BigIntegerField(
        verbose_name=domain.School.f_address_id.title,
        null=True,
    )
    u_address_id = models.BigIntegerField(
        verbose_name=domain.School.u_address_id.title,
        null=True,
    )
    telephone = models.CharField(
        verbose_name=domain.School.telephone.title,
        max_length=domain.School.telephone.max_length,
        null=True
    )
    fax = models.CharField(
        verbose_name=domain.School.fax.title,
        max_length=domain.School.fax.max_length,
        null=True
    )
    email = models.CharField(
        verbose_name=domain.School.email.title,
        max_length=domain.School.email.max_length,
        null=True
    )
    website = models.CharField(
        verbose_name=domain.School.website.title,
        max_length=domain.School.website.max_length,
        null=True
    )
    parent = models.ForeignKey(
        'self',
        verbose_name=domain.School.parent.title,
        null=True,
        on_delete=models.PROTECT
    )
    territory_type_id = models.BigIntegerField(
        verbose_name=domain.School.territory_type_id.title,
    )
    municipal_unit_id = models.BigIntegerField(
        verbose_name=domain.School.municipal_unit_id.title,
        null=True
    )
    person_id = models.BigIntegerField(
        verbose_name=domain.School.person_id.title,
    )
    status = models.BooleanField(
        verbose_name=domain.School.status.title,
    )

    class Meta:
        db_table = 'school'
        verbose_name = 'Организация'
        verbose_name_plural = 'Организациии'
