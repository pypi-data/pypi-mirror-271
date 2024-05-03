from typing import (
    Optional,
    Union,
)

from explicit.domain import (
    Unset,
    unset,
)
from explicit.messagebus.commands import (
    Command,
)


class CreateBbk(Command):

    code: str
    name: str
    parent_id: Optional[int]

    class Config:
        title = 'Команда создания раздела ББК'


class UpdateBbk(Command):

    id: int
    code: Union[str, Unset] = unset
    name: Union[str, Unset] = unset
    parent_id: Union[int, None, Unset] = unset

    class Config:
        title = 'Команда обновления раздела ББК'


class DeleteBbk(Command):

    id: int

    class Config:
        title = 'Команда удаления раздела ББК'
