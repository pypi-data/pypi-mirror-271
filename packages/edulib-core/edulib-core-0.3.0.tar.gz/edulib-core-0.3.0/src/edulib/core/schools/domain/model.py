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


class SchoolNotFound(Exception):

    def __init__(self, *args):
        super().__init__('Образовательная организация не найдена', *args)


@dataclass
class School:
    """Образовательная организация.

    Является проекцией сущностей внешних ИС.
    """

    id: Union[int, None] = identifier()
    external_id: int = Field(title='Глобальный идентификатор')
    short_name: str = Field(title='Краткое наименование', max_length=200)
    person_id: int = Field(title='Директор ОО')
    status: bool = Field(title='Статус ОО')
    name: Union[str, None] = Field(title='Наименование', defaul=None)
    inn: Union[str, None] = Field(title='ИНН', max_length=12, default=None)
    kpp: Union[str, None] = Field(title='КПП', max_length=9, default=None)
    okato: Union[str, None] = Field(title='ОКАТО', max_length=12, default=None)
    oktmo: Union[str, None] = Field(title='ОКТМО', max_length=11, default=None)
    okpo: Union[str, None] = Field(title='ОКПО', max_length=12, default=None)
    ogrn: Union[str, None] = Field(title='ОГРН', max_length=15, default=None)
    institution_type_id: Union[int, None] = Field(title='Тип организации', default=None)
    f_address_id: Union[int, None] = Field(title='Фактический адрес', default=None)
    u_address_id: Union[int, None] = Field(title='Юридический адрес', default=None)
    telephone: Union[str, None] = Field(title='Телефон', max_length=50, default=None)
    fax: Union[str, None] = Field(title='Факс ОО', max_length=50, default=None)
    email: Union[str, None] = Field(title='Эл. почта ОО', max_length=50, default=None)
    website: Union[str, None] = Field(title='Сайт ОО', max_length=200, default=None)
    parent: Union['School', None] = Field(title='Управляющая организация', default=None)
    territory_type_id: Union[int, None] = Field(title='Тип территории', default=None)
    municipal_unit_id: Union[int, None] = Field(title='Муниципальная единица', default=None)
