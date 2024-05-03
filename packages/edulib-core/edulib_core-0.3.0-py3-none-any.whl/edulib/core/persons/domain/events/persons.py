from typing import (
    Union,
)

from explicit.domain.model import (
    Unset,
    unset,
)
from explicit.messagebus.events import (
    Event,
)
from pydantic.dataclasses import (
    dataclass,
)


@dataclass
class _PersonEvent(Event):

    id: Union[int, None, Unset] = unset
    external_id: Union[str, Unset] = unset
    surname: Union[str, Unset] = unset
    firstname: Union[str, Unset] = unset
    patronymic: Union[str, None, Unset] = unset
    date_of_birth: Union[str, Unset] = unset
    inn: Union[str, None, Unset] = unset
    phone: Union[str, None, Unset] = unset
    email: Union[str, None, Unset] = unset
    snils: Union[str, None, Unset] = unset
    gender_id: Union[int, Unset] = unset
    perm_reg_addr_id: Union[int, None, Unset] = unset
    temp_reg_addr_id: Union[int, None, Unset] = unset


@dataclass
class PersonCreated(_PersonEvent):
    """Физлицо создано."""


@dataclass
class PersonUpdated(_PersonEvent):
    """Физлицо обновлено."""


@dataclass
class PersonDeleted(_PersonEvent):
    """Физлицо удалено."""
