from typing import (
    TYPE_CHECKING,
)

from edulib.core.utils.tools import (
    modify,
)

from .factories import (
    EventDTO,
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from .model import (
        Event,
    )


def create_event(data: EventDTO, uow: 'UnitOfWork') -> 'Event':
    """Сервис создания плана работы библиотеки."""
    event = factory.create(data)

    return uow.events.add(event)


def update_event(data: EventDTO, uow: 'UnitOfWork') -> 'Event':
    """Сервис обновления плана работы библиотеки."""
    event = uow.events.get_object_by_id(data.id)
    modify(event, **data.dict(exclude={'id'}))

    return uow.events.update(event)


def delete_event(data: EventDTO, uow: 'UnitOfWork') -> None:
    """Сервис удаления плана работы библиотеки."""
    event = uow.events.get_object_by_id(data.id)
    uow.events.delete(event)
