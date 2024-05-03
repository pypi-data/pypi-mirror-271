import datetime
from typing import (
    Optional,
    Union,
)

from explicit.contrib.domain.model.fields import (
    identifier,
)
from pydantic import (
    Field,
)
from pydantic.dataclasses import dataclass  # noqa


class PupilNotFound(Exception):

    """Возбуждается, когда учащийся не может быть определен."""

    def __init__(self, *args):
        super().__init__('Учащийся не найден', *args)


@dataclass
class Pupil:

    """Учащийся.

    Является проекцией сущностей внешних ИС.
    """

    id: Union[int, None] = identifier()
    external_id: str = Field(title='Глобальный идентификатор ФЛ', max_length=36)
    training_begin_date: datetime.date = Field(title='Дата поступления')
    training_end_date: Optional[datetime.date] = Field(title='Дата выпуска', default=None)
    schoolchild_id: int = Field(title='Школьник')
    class_year_id: int = Field(title='Учебный класс')  # noqa
    school_id: int = Field(title='Организация')
