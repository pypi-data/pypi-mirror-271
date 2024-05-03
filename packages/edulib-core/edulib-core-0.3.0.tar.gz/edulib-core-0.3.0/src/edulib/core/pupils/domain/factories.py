import datetime
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
    Pupil,
)


class PupilDTO(DTOBase):

    external_id: Union[str, Unset] = unset
    training_begin_date: Union[datetime.date, Unset] = unset
    training_end_date: Union[Optional[datetime.date], Unset] = unset
    schoolchild_id: Union[int, Unset] = unset
    class_year_id: Union[int, Unset] = unset  # noqa
    school_id: Union[int, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: PupilDTO) -> Pupil:
        return Pupil(**data.dict())


factory = Factory()
