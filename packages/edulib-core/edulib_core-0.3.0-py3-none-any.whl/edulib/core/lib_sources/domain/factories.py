from typing import (
    Union,
)

from explicit.domain import (
    AbstractDomainFactory,
    DTOBase,
    Unset,
    unset,
)

from edulib.core.lib_sources.domain.model import (
    Source,
)


class SourceDTO(DTOBase):

    id: Union[int, None, Unset] = unset
    name: Union[str, Unset] = unset
    school_id: Union[int, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: SourceDTO) -> Source:
        return Source(**data.dict())


factory = Factory()
