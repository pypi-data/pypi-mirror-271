from typing import (
    Optional,
)

from explicit.contrib.domain.model import (
    identifier,
)
from pydantic import (
    Field,
    validator,
)
from pydantic.dataclasses import (
    dataclass,
)


class BbkNotFound(Exception):
    """Возбуждается, когда раздел ББК не может быть определен."""

    def __init__(self, *args):
        super().__init__('Раздел ББК не найден', *args)


@dataclass(config={'validate_assignment': True})
class Bbk:

    id: Optional[int] = identifier()
    code: str = Field(
        title='Код',
        max_length=20,
    )
    name: str = Field(
        title='Наименование',
        max_length=200,
    )
    parent_id: Optional[int] = Field(
        title='Родительский раздел',
    )

    @validator('code', 'name')
    def not_empty(cls, value, field):  # pylint: disable=no-self-argument
        text = value.strip()
        if text == '':
            raise ValueError(f'{field.field_info.title} не может быть пустым')

        return text
