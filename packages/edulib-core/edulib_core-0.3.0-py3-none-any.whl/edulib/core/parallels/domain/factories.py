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
    Parallel,
)


class ParallelDTO(DTOBase):

    title: Union[str, Unset] = unset
    external_id: Union[int, Unset] = unset
    system_object_id: Union[int, Unset] = unset
    object_status: Union[bool, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: ParallelDTO) -> Parallel:
        return Parallel(**data.dict())


factory = Factory()
