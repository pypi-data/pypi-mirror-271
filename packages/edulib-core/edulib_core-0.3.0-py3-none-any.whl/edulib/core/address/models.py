from django.db import (
    models,
)

from edulib.core.address.services.validators import (
    corps_validator,
    house_validator,
)
from edulib.core.base.models import (
    BaseModel,
)


class Address(BaseModel):
    """Адрес."""

    place = models.UUIDField(
        null=True,
        blank=True,
        verbose_name='Населенный пункт'
    )
    street = models.UUIDField(
        null=True,
        blank=True,
        verbose_name='Улица'
    )
    house = models.UUIDField(
        null=True,
        blank=True,
        verbose_name='Дом'
    )
    house_num = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        validators=[house_validator],
        verbose_name='Номер дома'
    )

    house_corps = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        validators=[corps_validator],
        verbose_name='Корпус дома,'
    )
    flat = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Квартира'
    )
    zip_code = models.CharField(
        max_length=6,
        null=True,
        blank=True,
        verbose_name='Индекс'
    )
    full = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        verbose_name='Адрес'
    )

    __hash__ = BaseModel.__hash__

    def __bool__(self):
        """
        Проверка на наличие данных. Вызывается при bool(obj).
        """
        return any((
            self.id,
            self.place,
            self.street,
            self.house,
            self.full,
        ))

    def __eq__(self, other):
        """Сравнение двух адресов."""
        if not isinstance(other, Address):
            return False

        is_equal = self.place == other.place and self.street == other.street

        if is_equal:
            # Проверяем совпадение по номеру дома
            if self.house and other.house:
                is_equal = self.house == other.house
            elif self.house_num and other.house_num:
                is_equal = self.house_num == other.house_num
            else:
                is_equal = False

            # Если в адресах указана квартира, то сверим квартиры
            if self.flat and other.flat:
                is_equal = self.flat == other.flat

            # Если в адресах указан индекс, то сверим индексы
            if self.zip_code and other.zip_code:
                is_equal = self.zip_code == other.zip_code

        return is_equal

    class Meta:  # noqa: D106
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
