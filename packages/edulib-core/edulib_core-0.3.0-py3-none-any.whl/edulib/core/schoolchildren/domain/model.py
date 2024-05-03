from typing import (
    Union,
)

from explicit.contrib.domain.model.fields import (
    identifier,
)
from pydantic import (
    Field,
)
from pydantic.dataclasses import dataclass  # noqa


class SchoolchildNotFound(Exception):

    """Возбуждается, когда учащийся не может быть определен."""

    def __init__(self, *args):
        super().__init__('Учащийся школы не найден', *args)


@dataclass
class Schoolchild:

    """Учащийся школы."""

    id: Union[int, None] = identifier()
    person_id: int = Field(title='Физлицо')
