from typing import (
    Optional,
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
class _ClassYearEvent(Event):

    external_id: Union[str, Unset] = unset
    school_id: Union[int, Unset] = unset
    name: Union[str, Unset] = unset
    parallel_id: Union[int, Unset] = unset
    letter: Optional[Union[str, Unset]] = unset
    teacher_id: Optional[Union[int, Unset]] = unset
    academic_year_id: Union[int, Unset] = unset
    open_at: Union[str, Unset] = unset
    close_at: Optional[Union[str, Unset]] = unset


@dataclass
class ClassYearCreated(_ClassYearEvent):
    """Класс создан."""


@dataclass
class ClassYearUpdated(_ClassYearEvent):
    """Класс обновлен."""


@dataclass
class ClassYearDeleted(_ClassYearEvent):
    """Класс удален."""
