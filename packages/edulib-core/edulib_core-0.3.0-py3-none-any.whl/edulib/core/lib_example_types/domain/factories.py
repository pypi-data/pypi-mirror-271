from typing import (
    Union,
)

from explicit.domain import (
    AbstractDomainFactory,
    DTOBase,
    Unset,
    unset,
)

from .model import (
    ExampleType,
    ReleaseMethod,
)


class ExampleTypeDTO(DTOBase):

    id: Union[int, Unset] = unset
    code: Union[str, Unset] = unset
    name: Union[str, Unset] = unset
    release_method: Union[ReleaseMethod, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: ExampleTypeDTO) -> ExampleType:
        return ExampleType(**data.dict())


factory = Factory()
