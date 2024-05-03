from typing import (
    Union,
)
from uuid import (
    UUID,
)

from explicit.contrib.domain.model.fields import (
    identifier,
)
from pydantic import (
    Field,
)
from pydantic.dataclasses import (
    dataclass,
)


class AddressNotFound(Exception):

    def __init__(self, *args):
        super().__init__('Адрес не найден', *args)


@dataclass
class Address:
    """Адрес."""

    id: Union[int, None] = identifier()
    place: Union[UUID, None] = Field(default=None, title='Населенный пункт')
    street: Union[UUID, None] = Field(default=None, title='Улица')
    house: Union[UUID, None] = Field(default=None, title='Дом')
    house_num: Union[str, None] = Field(default=None, title='Номер дома', max_length=20)
    house_corps: Union[str, None] = Field(default=None, title='Корпус дома', max_length=10)
    flat: Union[str, None] = Field(default=None, title='Квартира', max_length=50)
    zip_code: Union[str, None] = Field(default=None, title='Индекс', max_length=6)
    full: Union[str, None] = Field(default=None, title='Адрес', max_length=300)
