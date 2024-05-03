from typing import (
    TYPE_CHECKING,
)

from edulib.core.lib_publishings.domain.factories import (
    PublishingDTO,
    factory,
)
from edulib.core.utils.tools import (
    modify,
)


if TYPE_CHECKING:
    from edulib.core.lib_publishings.domain.model import (
        Publishing,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def create_publishing(data: PublishingDTO, uow: 'UnitOfWork') -> 'Publishing':
    """Сервис создания издательства."""
    publishing = factory.create(data)
    uow.publishings.add(publishing)
    assert publishing.id is not None, publishing

    return publishing


def update_publishing(data: PublishingDTO, uow: 'UnitOfWork') -> 'Publishing':
    """Сервис обновления издательства."""
    publishing = uow.publishings.get_object_by_id(data.id)
    modify(publishing, **data.dict(exclude={'id'}))
    uow.publishings.update(publishing)

    return publishing


def delete_publishing(data: PublishingDTO, uow: 'UnitOfWork') -> None:
    """Сервис удаления издательства."""
    publishing = uow.publishings.get_object_by_id(data.id)
    uow.publishings.delete(publishing)
