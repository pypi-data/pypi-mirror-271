from datetime import (
    date,
)
from typing import (
    Optional,
    Union,
)

from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
)
from explicit.domain import (
    Unset,
    unset,
)
from explicit.messagebus.commands import (
    Command,
)


class CreateEvent(Command):

    place: str
    participants: str
    name: str
    library_id: int
    file: Optional[InMemoryUploadedFile]
    description: Optional[str]
    date_begin: date
    date_end: Optional[date]

    class Config:
        title = 'Команда создания плана работы библиотеки'
        arbitrary_types_allowed = True


class UpdateEvent(Command):

    id: int
    place: Union[str, Unset] = unset
    participants: Union[str, Unset] = unset
    name: Union[str, Unset] = unset
    library_id: Union[int, Unset] = unset
    file: Union[InMemoryUploadedFile, None, Unset] = unset
    description: Union[str, None, Unset] = unset
    date_begin: Union[date, Unset] = unset
    date_end: Union[date, None, Unset] = unset

    class Config:
        title = 'Команда обновления плана работы библиотеки'
        arbitrary_types_allowed = True


class DeleteEvent(Command):

    id: int

    class Config:
        title = 'Команда удаления плана работы библиотеки'
