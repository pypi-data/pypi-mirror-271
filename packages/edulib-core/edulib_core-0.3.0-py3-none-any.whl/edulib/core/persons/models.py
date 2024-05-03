from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)

from . import (
    domain,
)


class Person(BaseModel):

    """Проекция "Физическое лицо"."""

    external_id = models.CharField(
        verbose_name=domain.Person.external_id.title,
        max_length=domain.Person.external_id.max_length,
        db_index=True,
    )
    surname = models.CharField(
        verbose_name=domain.Person.surname.title,
        max_length=domain.Person.surname.max_length,
        db_index=True,
    )
    firstname = models.CharField(
        verbose_name=domain.Person.firstname.title,
        max_length=domain.Person.firstname.max_length,
        db_index=True,
    )
    patronymic = models.CharField(
        verbose_name=domain.Person.patronymic.title,
        max_length=domain.Person.patronymic.max_length,
        null=True, blank=True,
        db_index=True,
    )
    date_of_birth = models.DateField(
        verbose_name=domain.Person.date_of_birth.title,
        db_index=True
    )
    inn = models.CharField(
        verbose_name=domain.Person.inn.title,
        max_length=domain.Person.inn.max_length,
        null=True, blank=True,
    )
    phone = models.CharField(
        verbose_name=domain.Person.phone.title,
        max_length=domain.Person.phone.max_length,
        null=True, blank=True
    )
    email = models.CharField(
        max_length=domain.Person.email.max_length,
        null=True, blank=True
    )
    snils = models.CharField(
        verbose_name=domain.Person.snils.title,
        max_length=domain.Person.snils.max_length,
        default=domain.Person.snils.default,
        blank=True,
        db_index=True,
    )
    gender_id = models.BigIntegerField(
        verbose_name=domain.Person.gender_id.title,
    )
    perm_reg_addr_id = models.BigIntegerField(
        verbose_name=domain.Person.perm_reg_addr_id.title,
        null=True, blank=True
    )
    temp_reg_addr_id = models.BigIntegerField(
        verbose_name=domain.Person.temp_reg_addr_id.title,
        null=True, blank=True
    )

    class Meta:
        db_table = 'person'
        indexes = (
            models.Index(fields=['surname', 'firstname', 'patronymic']),
        )
        verbose_name = 'Физическое лицо'
        verbose_name_plural = 'Физические лица'
