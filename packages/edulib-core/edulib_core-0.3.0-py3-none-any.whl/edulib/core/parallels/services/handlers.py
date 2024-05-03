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
    from edulib.core.parallels.domain import (
        ParallelCreated,
        ParallelDeleted,
        ParallelUpdated,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def on_parallel_created(
    event: 'ParallelCreated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.create_parallel(domain.ParallelDTO(**asdict(event)), uow)


def on_parallel_updated(
    event: 'ParallelUpdated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.update_parallel(domain.ParallelDTO(**asdict(event)), uow)


def on_parallel_deleted(
    event: 'ParallelDeleted',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.delete_parallel(domain.ParallelDTO(**asdict(event)), uow)
