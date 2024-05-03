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
    from edulib.core.municipal_units.domain import (
        MunicipalUnitCreated,
        MunicipalUnitDeleted,
        MunicipalUnitUpdated,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def on_municipal_unit_created(
    event: 'MunicipalUnitCreated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.create_municipal_unit(domain.MunicipalUnitDTO(**asdict(event)), uow)


def on_municipal_unit_updated(
    event: 'MunicipalUnitUpdated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.update_municipal_unit(domain.MunicipalUnitDTO(**asdict(event)), uow)


def on_municipal_unit_deleted(
    event: 'MunicipalUnitDeleted',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.delete_municipal_unit(domain.MunicipalUnitDTO(**asdict(event)), uow)
