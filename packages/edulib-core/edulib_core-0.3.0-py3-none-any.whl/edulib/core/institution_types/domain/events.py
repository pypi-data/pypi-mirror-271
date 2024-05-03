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
class InstitutionTypeEvent(Event):

    external_id: Union[str, Unset] = unset
    code: Union[str, Unset] = unset
    name: Union[str, None, Unset] = unset


@dataclass
class InstitutionTypeCreated(InstitutionTypeEvent):
    """Тип организации создан."""


@dataclass
class InstitutionTypeUpdated(InstitutionTypeEvent):
    """Тип организации обновлен."""


@dataclass
class InstitutionTypeDeleted(InstitutionTypeEvent):
    """Тип организации удален."""
