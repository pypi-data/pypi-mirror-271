from typing import (
    Union,
)

from explicit.domain.model import (
    Unset,
    unset,
)
from explicit.messagebus.commands import (
    Command,
)


class _AddressCommand(Command):

    id: Union[int, Unset] = unset
    place: Union[str, None, Unset] = unset
    street: Union[str, None, Unset] = unset
    house: Union[str, None, Unset] = unset
    house_num: Union[str, None, Unset] = unset
    house_corps: Union[str, None, Unset] = unset
    flat: Union[str, None, Unset] = unset
    zip_code: Union[str, None, Unset] = unset
    full: Union[str, None, Unset] = unset


class CreateAddress(_AddressCommand):
    """Команда "Создать адрес"."""


class UpdateAddress(_AddressCommand):
    """Команда "Обновить адрес"."""


class DeleteAddress(_AddressCommand):
    """Команда "Удалить адрес"."""
