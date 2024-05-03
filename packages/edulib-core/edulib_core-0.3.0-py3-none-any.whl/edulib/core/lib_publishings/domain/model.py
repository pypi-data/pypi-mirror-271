from typing import (
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


class PublishingNotFound(Exception):
    """Возбуждается, когда издательство не может быть определено."""

    def __init__(self, *args):
        super().__init__('Издательство не найдено', *args)


@dataclass
class Publishing:

    id: Optional[int] = identifier()
    name: str = Field(
        title='Издательство',
        max_length=256,
    )
