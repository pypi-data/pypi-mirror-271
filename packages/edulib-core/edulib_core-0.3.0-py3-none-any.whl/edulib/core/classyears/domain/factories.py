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
    ClassYear,
)


class ClassYearDTO(DTOBase):

    external_id: Union[str, Unset] = unset
    school_id: Union[int, Unset] = unset
    name: Union[str, Unset] = unset
    parallel_id: Union[int, Unset] = unset
    letter: Optional[Union[str, Unset]] = unset
    teacher_id: Optional[Union[int, Unset]] = unset
    academic_year_id: Union[int, Unset] = unset
    open_at: Union[str, Unset] = unset
    close_at: Optional[Union[str, Unset]] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: ClassYearDTO) -> ClassYear:
        params = data.dict()
        return ClassYear(**params)


factory = Factory()
