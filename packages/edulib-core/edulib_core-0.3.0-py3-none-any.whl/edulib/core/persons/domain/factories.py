import datetime
from typing import (
    Union,
)

from explicit.domain.factories import (
    AbstractDomainFactory,
    DTOBase,
)
from explicit.domain.model import (
    Unset,
    unset,
)

from .model import (
    Person,
)


class PersonDTO(DTOBase):

    id: Union[int, None, Unset] = unset
    external_id: Union[str, Unset] = unset
    surname: Union[str, Unset] = unset
    firstname: Union[str, Unset] = unset
    patronymic: Union[str, None, Unset] = unset
    date_of_birth: Union[datetime.date, Unset] = unset
    inn: Union[str, None, Unset] = unset
    phone: Union[str, None, Unset] = unset
    email: Union[str, None, Unset] = unset
    snils: Union[str, None, Unset] = unset
    gender_id: Union[int, Unset] = unset
    perm_reg_addr_id: Union[int, None, Unset] = unset
    temp_reg_addr_id: Union[int, None, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: PersonDTO) -> Person:
        params = data.dict()
        return Person(**params)


factory = Factory()
