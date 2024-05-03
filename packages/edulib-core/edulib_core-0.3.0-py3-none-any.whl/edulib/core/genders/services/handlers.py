from typing import (
    TYPE_CHECKING,
)

from explicit.domain.model import (
    asdict,
)

from .. import (
    domain,
)


if TYPE_CHECKING:
    from edulib.core.genders.domain import (
        GenderCreated,
        GenderDeleted,
        GenderUpdated,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def on_gender_created(
    event: 'GenderCreated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.create_gender(domain.GenderDTO(**asdict(event)), uow)


def on_gender_updated(
    event: 'GenderUpdated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.update_gender(domain.GenderDTO(**asdict(event)), uow)


def on_gender_deleted(
    event: 'GenderDeleted',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.delete_gender(domain.GenderDTO(**asdict(event)), uow)
