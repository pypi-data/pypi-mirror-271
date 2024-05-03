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
    School,
)


class SchoolDTO(DTOBase):

    external_id: Union[int, Unset] = unset
    name: Union[str, None, Unset] = unset
    short_name: Union[str, Unset] = unset
    person_id: Union[int, Unset] = unset
    status: Union[bool, Unset] = unset
    inn: Union[str, None, Unset] = unset
    kpp: Union[str, None, Unset] = unset
    okato: Union[str, None, Unset] = unset
    oktmo: Union[str, None, Unset] = unset
    okpo: Union[str, None, Unset] = unset
    ogrn: Union[str, None, Unset] = unset
    institution_type_id: Union[int, None, Unset] = unset
    f_address_id: Union[int, None, Unset] = unset
    u_address_id: Union[int, None, Unset] = unset
    telephone: Union[str, None, Unset] = unset
    fax: Union[str, None, Unset] = unset
    email: Union[str, None, Unset] = unset
    website: Union[str, None, Unset] = unset
    parent_id: Union[int, None, Unset] = unset
    territory_type_id: Union[int, None, Unset] = unset
    municipal_unit_id: Union[int, None, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: SchoolDTO) -> School:
        return School(**data.dict())


factory = Factory()
