from typing import (
    Optional,
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


class SourceNotFound(Exception):
    """Возбуждается, когда источник поступления в библиотеку не может быть определен."""

    def __init__(self, *args):
        super().__init__('Источник поступления в библиотеку не найден', *args)


@dataclass
class Source:

    id: Optional[int] = identifier()
    name: str = Field(
        title='Источник поступления',
        max_length=256,
    )
    school_id: int = Field(
        title='Организация',
    )

    class Config:
        title = 'Источник поступления'
