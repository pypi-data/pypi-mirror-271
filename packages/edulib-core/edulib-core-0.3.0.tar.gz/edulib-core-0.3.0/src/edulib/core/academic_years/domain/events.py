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
class AcademicYearEvent(Event):

    external_id: Union[str, Unset] = unset
    code: Union[str, Unset] = unset
    name: Union[str, None, Unset] = unset
    date_begin: Union[str, Unset] = unset
    date_end: Union[str, Unset] = unset


@dataclass
class AcademicYearCreated(AcademicYearEvent):
    """Учебный год создан."""


@dataclass
class AcademicYearUpdated(AcademicYearEvent):
    """Учебный год обновлен."""


@dataclass
class AcademicYearDeleted(AcademicYearEvent):
    """Учебный год удален."""
