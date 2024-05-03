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
        MunicipalUnitDTO,
    )
    from .model import (
        MunicipalUnit,
    )


def create_municipal_unit(data: 'MunicipalUnitDTO', uow: 'UnitOfWork') -> 'MunicipalUnit':
    municipal_unit = factory.create(data)

    if data.parent_id:
        municipal_unit.parent = uow.municipal_units.get_object_by_id(data.parent_id)

    uow.municipal_units.add(municipal_unit)
    assert municipal_unit.id is not None, municipal_unit

    return municipal_unit


def update_municipal_unit(data: 'MunicipalUnitDTO', uow: 'UnitOfWork') -> 'MunicipalUnit':
    municipal_unit = uow.municipal_units.get_by_external_id(data.external_id)

    changes = data.dict(exclude={'id'})

    modify(municipal_unit, **changes)
    if 'parent_id' in changes:
        parent_id = changes['parent_id']
        municipal_unit.parent = (
            uow.municipal_units.get_object_by_id(parent_id) if parent_id is not None
            else None
        )

    return uow.municipal_units.update(municipal_unit)


def delete_municipal_unit(data: 'MunicipalUnitDTO', uow: 'UnitOfWork'):
    municipal_unit = uow.municipal_units.get_by_external_id(data.external_id)

    return uow.municipal_units.delete(municipal_unit)
