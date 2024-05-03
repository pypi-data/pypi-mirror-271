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
    Schoolchild,
)


class SchoolchildDTO(DTOBase):

    person_id: Union[int, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: SchoolchildDTO) -> Schoolchild:
        params = data.dict()
        return Schoolchild(**params)


factory = Factory()
