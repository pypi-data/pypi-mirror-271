from typing import (
    Optional,
)

from explicit.domain.factories import (
    AbstractDomainFactory,
    DTOBase,
)

from edulib.core.lib_authors.domain.model import (
    Author,
)


class AuthorDTO(DTOBase):

    id: Optional[int] = None
    name: str

    class Config:
        arbitrary_types_allowed = False


class Factory(AbstractDomainFactory):

    def create(self, data: AuthorDTO) -> Author:
        return Author(**data.dict())


factory = Factory()
