from datetime import (
    date,
)
from typing import (
    Union,
)

from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
)
from explicit.domain import (
    AbstractDomainFactory,
    DTOBase,
    Unset,
    unset,
)

from .model import (
    Event,
)


class EventDTO(DTOBase):

    id: Union[int, None, Unset] = unset
    place: Union[str, Unset] = unset
    participants: Union[str, Unset] = unset
    name: Union[str, Unset] = unset
    library_id: Union[int, Unset] = unset
    file: Union[InMemoryUploadedFile, None, Unset] = unset
    description: Union[str, None, Unset] = unset
    date_begin: Union[date, Unset] = unset
    date_end: Union[date, None, Unset] = unset

    class Config:
        arbitrary_types_allowed = True


class Factory(AbstractDomainFactory):

    def create(self, data: EventDTO) -> Event:
        return Event(**data.dict())


factory = Factory()
