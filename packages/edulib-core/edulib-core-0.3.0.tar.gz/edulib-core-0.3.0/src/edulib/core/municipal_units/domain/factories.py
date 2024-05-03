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
    MunicipalUnit,
)


class MunicipalUnitDTO(DTOBase):

    external_id: Union[int, Unset] = unset
    code: Union[str, Unset] = unset
    name: Union[str, Unset] = unset
    constituent_entity: Union[str, Unset] = unset
    parent_id: Union[int, None, Unset] = unset
    okato: Union[str, Unset] = unset
    oktmo: Union[str, Unset] = unset


class MunicipalUnitFactory(AbstractDomainFactory):

    def create(self, data: MunicipalUnitDTO) -> MunicipalUnit:
        return MunicipalUnit(**data.dict())


factory = MunicipalUnitFactory()
