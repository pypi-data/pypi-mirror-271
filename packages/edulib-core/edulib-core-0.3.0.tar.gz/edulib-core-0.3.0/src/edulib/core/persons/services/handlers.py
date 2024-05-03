from typing import (
    TYPE_CHECKING,
)

from explicit.domain.model import (
    asdict,
)

from edulib.core import (
    logger,
)

from .. import (
    domain,
)


if TYPE_CHECKING:
    from edulib.core.persons.domain.events import (
        PersonCreated,
        PersonDeleted,
        PersonUpdated,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def null_handler(event: 'Event', uow: 'AbstractUnitOfWork') -> None:
    logger.info('Обработка события %s пропущена', type(event))


def on_person_created(
    event: 'PersonCreated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.create_person(domain.PersonDTO(**asdict(event)), uow)


def on_person_updated(
    event: 'PersonUpdated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.update_person(domain.PersonDTO(**asdict(event)), uow)


def on_person_deleted(
    event: 'PersonDeleted',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.delete_person(domain.PersonDTO(**asdict(event)), uow)
