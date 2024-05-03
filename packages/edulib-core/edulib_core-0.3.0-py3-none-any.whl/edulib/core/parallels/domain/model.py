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


class ParallelNotFound(Exception):

    def __init__(self, *args):
        super().__init__('Параллель не найдена', *args)


@dataclass
class Parallel:
    """Параллель.

    Является проекцией сущностей внешних ИС.
    """

    id: Union[int, None] = identifier()
    title: str = Field(title='Наименование', max_length=20)
    external_id: int = Field(title='Глобальный идентификатор')
    system_object_id: int = Field(title='Идентификатор')
    object_status: bool = Field(title='Статус')
