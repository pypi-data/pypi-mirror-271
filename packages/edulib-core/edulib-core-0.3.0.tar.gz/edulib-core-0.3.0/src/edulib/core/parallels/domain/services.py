from typing import (
    TYPE_CHECKING,
)

from edulib.core.utils.tools import (
    modify,
)

from .factories import (
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from .factories import (
        ParallelDTO,
    )
    from .model import (
        Parallel,
    )


def create_parallel(data: 'ParallelDTO', uow: 'UnitOfWork') -> 'Parallel':
    parallel = factory.create(data)
    uow.parallels.add(parallel)
    assert parallel.id is not None, parallel

    return parallel


def update_parallel(data: 'ParallelDTO', uow: 'UnitOfWork') -> 'Parallel':
    parallel = uow.parallels.get_by_external_id(data.external_id)
    modify(parallel, **data.dict(exclude={'id'}))

    return uow.parallels.update(parallel)


def delete_parallel(data: 'ParallelDTO', uow: 'UnitOfWork'):
    parallel = uow.parallels.get_by_external_id(data.external_id)

    return uow.parallels.delete(parallel)
