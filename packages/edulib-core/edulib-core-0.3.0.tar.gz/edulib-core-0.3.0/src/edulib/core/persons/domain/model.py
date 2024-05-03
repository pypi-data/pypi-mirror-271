import datetime
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


class PersonNotFound(Exception):

    """Возбуждается, когда физлицо не может быть определено."""

    def __init__(self, *args):
        super().__init__('Физлицо не найдено', *args)


@dataclass
class Person:

    """Физлицо (Персона).

    Является проекцией сущностей внешних ИС.
    """

    id: Union[int, None] = identifier()
    external_id: str = Field(title='Глобальный идентификатор ФЛ', max_length=36)
    surname: str = Field(title='Фамилия', max_length=60)
    firstname: str = Field(title='Имя', max_length=60)
    patronymic: Union[str, None] = Field(title='Отчество', max_length=60, default=None)
    date_of_birth: datetime.date = Field(title='Дата рождения')
    inn: Union[str, None] = Field(title='ИНН', max_length=12, default=None)
    phone: Union[str, None] = Field(title='Мобильный телефон', max_length=50, default=None)
    email: Union[str, None] = Field(title='E-mail', max_length=50, default=None)
    snils: Union[str, None] = Field(title='СНИЛС', max_length=14, default='')
    gender_id: int = Field(title='Пол')
    perm_reg_addr_id: Union[int, None] = Field(title='Адрес регистрации по месту жительства', default=None)
    temp_reg_addr_id: Union[int, None] = Field(title='Адрес регистрации по месту пребывания', default=None)
