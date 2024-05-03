from datetime import (
    date,
)
from typing import (
    Any,
    Optional,
)

from explicit.contrib.domain.model import (
    identifier,
)
from pydantic import (
    Field,
)
from pydantic.dataclasses import (
    dataclass,
)


class EventNotFound(Exception):
    """Возбуждается, когда план работы библиотеки не может быть определен."""

    def __init__(self, *args):
        super().__init__('План работы библиотеки не найден', *args)


@dataclass
class Event:
    """План работы библиотеки."""

    id: Optional[int] = identifier()
    place: str = Field(
        title='Место проведения',
        max_length=100,
    )
    participants: str = Field(
        title='Заинтересованная аудитория/участники',
        max_length=100,
    )
    name: str = Field(
        title='Наименование',
        max_length=250,
    )
    library_id: int = Field(
        title='Библиотека',
    )
    file: Any = Field(
        title='Приложения',
    )
    description: Optional[str] = Field(
        title='Описание',
        default='',
    )
    date_begin: date = Field(
        title='Дата начала мероприятия',
    )
    date_end: Optional[date] = Field(
        title='Дата окончания мероприятия',
    )
