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


class ClassYearNotFound(Exception):

    """Возбуждается, когда класс не может быть определен."""

    def __init__(self, *args):
        super().__init__('Класс не найден', *args)


@dataclass
class ClassYear:

    """Класс.

    Является проекцией сущностей внешних ИС.
    """

    id: Union[int, None] = identifier()
    external_id: str = Field(title='Глобальный идентификатор', max_length=36)
    school_id: int = Field(title='Организация')
    name: str = Field(title='Наименование', max_length=200)
    parallel_id: int = Field(title='Параллель')
    letter: Union[str, None] = Field(title='Литер', max_length=20)
    teacher_id: Union[int, None] = Field(title='Идентификатор учителя', default=None)
    academic_year_id: int = Field(title='Идентификатор академического года')
    open_at: Union[datetime.date, None] = Field(title='Дата открытия класса', default=None)
    close_at: Union[datetime.date, None] = Field(title='Дата закрытия класса', default=None)
