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


class InfoProductMarkNotFound(Exception):
    """Возбуждается, когда знак информационной продукции не может быть определен"""

    def __init__(self, *args):
        super().__init__('Знак информационной продукции не найден', *args)


@dataclass
class InfoProductMark:

    id: Optional[int] = identifier()
    code: str = Field(
        title='Код',
        max_length=20,
    )
    name: str = Field(
        title='Наименование',
        max_length=200,
    )
