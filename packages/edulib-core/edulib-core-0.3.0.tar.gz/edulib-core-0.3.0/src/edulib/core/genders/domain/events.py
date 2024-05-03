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
class GenderEvent(Event):

    external_id: Union[str, Unset] = unset
    code: Union[str, Unset] = unset
    name: Union[str, None, Unset] = unset


@dataclass
class GenderCreated(GenderEvent):
    """Пол создан."""


@dataclass
class GenderUpdated(GenderEvent):
    """Пол обновлен."""


@dataclass
class GenderDeleted(GenderEvent):
    """Пол удален."""
