from typing import (
    Optional,
    Union,
)

from explicit.domain import (
    AbstractDomainFactory,
    DTOBase,
    Unset,
    unset,
)

from .model import (
    Bbk,
)


class BbkDTO(DTOBase):

    id: Optional[int] = None
    code: Union[str, Unset] = unset
    name: Union[str, Unset] = unset
    parent_id: Union[int, None, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: BbkDTO) -> Bbk:
        return Bbk(**data.dict())


factory = Factory()
