import datetime
from typing import (
    Union,
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


class AcademicYearNotFound(Exception):
    """Возбуждается, когда учебный год не может быть определен."""

    def __init__(self, *args):
        super().__init__('Учебный год не найден', *args)


@dataclass
class AcademicYear:
    """Учебный год.

    Является проекцией сущностей внешних ИС.
    """

    id: Union[int, None] = identifier()
    external_id: str = Field(title='Глобальный идентификатор', max_length=36)
    code: str = Field(title='Код', max_length=50)
    name: Union[str, None] = Field(title='Наименование', max_length=200)
    date_begin: datetime.date = Field(title='Дата начала')
    date_end: datetime.date = Field(title='Дата окончания')
