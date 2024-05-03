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
    Address,
)


class AddressDTO(DTOBase):

    id: Union[int, None, Unset] = unset
    place: Union[str, None, Unset] = unset
    street: Union[str, None, Unset] = unset
    house: Union[str, None, Unset] = unset
    house_num: Union[str, None, Unset] = unset
    house_corps: Union[str, None, Unset] = unset
    flat: Union[str, None, Unset] = unset
    zip_code: Union[str, None, Unset] = unset
    full: Union[str, None, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: AddressDTO) -> Address:
        params = data.dict()
        return Address(**params)


factory = Factory()
