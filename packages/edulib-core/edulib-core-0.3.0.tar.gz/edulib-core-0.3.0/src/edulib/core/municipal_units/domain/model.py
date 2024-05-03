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


class MunicipalUnitNotFound(Exception):

    def __init__(self, *args):
        super().__init__('Муниципальная единица не найдена', *args)


@dataclass
class MunicipalUnit:
    """Муниципальная единица.

    Является проекцией сущностей внешних ИС.
    """

    id: Union[int, None] = identifier()
    external_id: int = Field(title='Глобальный идентификатор')
    code: str = Field(title='Код', max_length=20)
    name: str = Field(title='Наименование')
    parent: Union['MunicipalUnit', None] = Field(title='Родительская организация', default=None)
    constituent_entity: str = Field(title='Наименование субъекта РФ', max_length=200)
    okato: str = Field(title='ОКАТО', max_length=12)
    oktmo: str = Field(title='ОКТМО', max_length=11)
