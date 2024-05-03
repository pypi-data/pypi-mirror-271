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
        AddressDTO,
    )
    from .model import (
        Address,
    )


def create_address(data: 'AddressDTO', uow: 'UnitOfWork') -> 'Address':
    address = factory.create(data)
    uow.addresses.add(address)
    assert address.id is not None, address

    return address


def update_address(data: 'AddressDTO', uow: 'UnitOfWork') -> 'Address':
    address = uow.addresses.get_object_by_id(data.id)
    modify(address, **data.dict(exclude={'id'}))

    return uow.addresses.update(address)


def delete_address(data: 'AddressDTO', uow: 'UnitOfWork'):
    address = uow.addresses.get_object_by_id(data.id)

    return uow.addresses.delete(address)
