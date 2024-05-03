import datetime
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
class _PupilEvent(Event):

    external_id: Union[str, Unset] = unset
    person_id: Union[str, Unset] = unset
    training_begin_date: Union[datetime.date, Unset] = unset
    training_end_date: Union[datetime.date, None, Unset] = unset
    schoolchild_id: Union[int, Unset] = unset
    class_year_id: Union[int, Unset] = unset  # noqa
    class_external_id: Union[str, Unset] = unset  # noqa
    school_id: Union[int, Unset] = unset


@dataclass
class PupilCreated(_PupilEvent):
    """Учащийся создан."""


@dataclass
class PupilUpdated(_PupilEvent):
    """Учащийся обновлен."""


@dataclass
class PupilDeleted(_PupilEvent):
    """Учащийся удален."""
