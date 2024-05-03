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
    from edulib.core.classyears.domain.events import (
        ClassYearCreated,
        ClassYearDeleted,
        ClassYearUpdated,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def on_classyear_created(
    event: 'ClassYearCreated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.create_classyear(domain.ClassYearDTO(**asdict(event)), uow)


def on_classyear_updated(
    event: 'ClassYearUpdated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.update_classyear(domain.ClassYearDTO(**asdict(event)), uow)


def on_classyear_deleted(
    event: 'ClassYearDeleted',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.delete_classyear(domain.ClassYearDTO(**asdict(event)), uow)
