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
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def create_address(
    command: domain.CreateAddress,
    uow: 'UnitOfWork'
) -> domain.Address:
    with uow.wrap():
        return domain.create_address(domain.AddressDTO(**asdict(command)), uow)


def update_address(
    command: domain.UpdateAddress,
    uow: 'UnitOfWork'
) -> domain.Address:
    with uow.wrap():
        return domain.update_address(domain.AddressDTO(**asdict(command)), uow)


def delete_address(
    command: domain.DeleteAddress,
    uow: 'UnitOfWork'
) -> domain.Address:
    with uow.wrap():
        return domain.delete_address(domain.AddressDTO(**asdict(command)), uow)
