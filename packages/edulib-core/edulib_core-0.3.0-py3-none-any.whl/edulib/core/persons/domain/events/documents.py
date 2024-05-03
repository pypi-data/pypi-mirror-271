from typing import (
    Optional,
    Union,
)

from explicit.domain.model import (
    Unset,
    unset,
)
from explicit.messagebus.events import (
    Event,
)
from pydantic.dataclasses import (
    dataclass,
)


@dataclass
class _PersonDocumentEvent(Event):

    person_id: Optional[Union[str, Unset]] = unset
    document_type_id: Union[int, Unset] = unset
    number: Union[str, Unset] = unset

    series: Optional[Union[str, Unset]] = unset
    subdivision_code: Optional[Union[str, Unset]] = unset
    issuer: Optional[Union[str, Unset]] = unset
    issued: Optional[Union[str, Unset]] = unset
    expiration: Optional[Union[str, Unset]] = unset

    document_type: Optional[dict] = None


@dataclass
class PersonDocumentCreated(_PersonDocumentEvent):
    """Документ ФЛ создан."""


@dataclass
class PersonDocumentUpdated(_PersonDocumentEvent):
    """Документ ФЛ обновлен."""


@dataclass
class PersonDocumentDeleted(_PersonDocumentEvent):
    """Документ ФЛ удален."""
