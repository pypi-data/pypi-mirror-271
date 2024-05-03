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
class ParallelEvent(Event):

    title: Union[str, Unset] = unset
    external_id: Union[int, Unset] = unset
    system_object_id: Union[int, Unset] = unset
    object_status: Union[bool, Unset] = unset


@dataclass
class ParallelCreated(ParallelEvent):
    """Параллель создана."""


@dataclass
class ParallelUpdated(ParallelEvent):
    """Параллель обновлена."""


@dataclass
class ParallelDeleted(ParallelEvent):
    """Параллель удалена."""
