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


class GenderNotFound(Exception):
    """Возбуждается, когда пол не может быть определен."""

    def __init__(self, *args):
        super().__init__('Пол не найден', *args)


@dataclass
class Gender:
    """Пол.

    Является проекцией сущностей внешних ИС.
    """

    id: Union[int, None] = identifier()
    external_id: str = Field(title='Глобальный идентификатор', max_length=36)
    code: str = Field(title='Код', max_length=20)
    name: Union[str, None] = Field(title='Наименование', max_length=200)
