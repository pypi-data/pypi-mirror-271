from typing import (
    Union,
)

from explicit.domain import (
    AbstractDomainFactory,
    DTOBase,
    Unset,
    unset,
)

from edulib.core.lib_publishings.domain.model import (
    Publishing,
)


class PublishingDTO(DTOBase):

    id: Union[int, None, Unset] = unset
    name: Union[str, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: PublishingDTO) -> Publishing:
        return Publishing(**data.dict())


factory = Factory()
