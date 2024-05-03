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


class AuthorNotFound(Exception):
    """Возбуждается, когда автор не может быть определен."""

    def __init__(self, *args):
        super().__init__('Автор не найден', *args)


@dataclass
class Author:

    id: Optional[int] = identifier()
    name: str = Field(
        title='Автор',
        max_length=256,
    )

    class Config:
        title = 'Автор'
