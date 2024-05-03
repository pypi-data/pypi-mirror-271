from typing import (
    Union,
)

from explicit.domain import (
    Unset,
    unset,
)
from explicit.messagebus.commands import (
    Command,
)


class CreateSource(Command):

    name: str
    school_id: int

    class Config:
        title = 'Команда создания источника поступления'


class UpdateSource(Command):

    id: int
    name: Union[str, Unset] = unset

    class Config:
        title = 'Команда обновления источника поступления'


class DeleteSource(Command):

    id: int

    class Config:
        title = 'Команда удаления источника поступления'
