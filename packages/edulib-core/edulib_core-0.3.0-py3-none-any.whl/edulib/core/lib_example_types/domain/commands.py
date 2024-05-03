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

from .model import (
    ReleaseMethod,
)


class CreateExampleType(Command):

    name: str
    release_method: ReleaseMethod = ReleaseMethod.PRINTED

    class Config:
        title = 'Команда создания типа библиотечных экземпляров'


class UpdateExampleType(Command):

    id: int
    name: Union[str, Unset] = unset
    release_method: Union[ReleaseMethod, Unset] = unset

    class Config:
        title = 'Команда обновления типа библиотечных экземпляров'


class DeleteExampleType(Command):

    id: int

    class Config:
        title = 'Команда удаления типа библиотечных экземпляров'
