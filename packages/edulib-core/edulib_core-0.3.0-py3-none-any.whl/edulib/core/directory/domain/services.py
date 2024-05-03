from typing import (
    TYPE_CHECKING,
)

from edulib.core.utils.tools import (
    modify,
)

from .factories import (
    BbkDTO,
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from .model import (
        Bbk,
    )


def create_bbk(data: BbkDTO, uow: 'UnitOfWork') -> 'Bbk':
    """Сервис создания раздела ББК."""
    bbk = factory.create(data)
    uow.bbk.add(bbk)
    assert bbk.id is not None, bbk

    return bbk


def update_bbk(data: BbkDTO, uow: 'UnitOfWork') -> 'Bbk':
    """Сервис обновления ББК."""
    publishing = uow.bbk.get_object_by_id(data.id)
    modify(publishing, **data.dict(exclude={'id'}))
    uow.bbk.update(publishing)

    return publishing


def delete_bbk(data: BbkDTO, uow: 'UnitOfWork') -> None:
    """Сервис удаления ББК."""
    bbk = uow.bbk.get_object_by_id(data.id)
    uow.bbk.delete(bbk)
