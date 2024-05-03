from typing import (
    Optional,
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
    Gender,
)


class GenderDTO(DTOBase):

    external_id: Union[str, Unset] = unset
    code: Union[str, Unset] = unset
    name: Optional[Union[str, Unset]] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: GenderDTO) -> Gender:
        return Gender(**data.dict())


factory = Factory()
