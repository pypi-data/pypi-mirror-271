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

from edulib.core.utils.enums import (
    NamedIntEnum,
)


class ExampleTypeNotFound(Exception):
    """Возбуждается, когда тип библиотечных экземпляров не может быть определен."""

    def __init__(self, *args):
        super().__init__('Тип библиотечных экземпляров не найден', *args)


class ReleaseMethod(NamedIntEnum):
    """Способ публикации экземпляров."""

    PRINTED = 1, 'Печатные'
    ELECTRONIC = 2, 'Электронные (медиафайл и др)'
    PERIODICAL = 3, 'Периодика'


@dataclass(config={'validate_assignment': True})
class ExampleType:
    """Тип библиотечных экземпляров."""

    id: Optional[int] = identifier()
    name: str = Field(
        title='Наименование',
        max_length=200,
    )
    release_method: ReleaseMethod = Field(
        title='Тип',
        default=ReleaseMethod.PRINTED,
    )

    @validator('name')
    def not_empty(cls, value, field):  # pylint: disable=no-self-argument
        text = value.strip()
        if text == '':
            raise ValueError(f'{field.field_info.title} не может быть пустым')

        return text
