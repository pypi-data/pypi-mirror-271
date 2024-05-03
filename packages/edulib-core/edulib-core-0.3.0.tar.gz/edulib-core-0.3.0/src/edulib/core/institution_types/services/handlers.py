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
    from edulib.core.institution_types.domain import (
        InstitutionTypeCreated,
        InstitutionTypeDeleted,
        InstitutionTypeUpdated,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def on_institution_type_created(
    event: 'InstitutionTypeCreated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.create_institution_type(domain.InstitutionTypeDTO(**asdict(event)), uow)


def on_institution_type_updated(
    event: 'InstitutionTypeUpdated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.update_institution_type(domain.InstitutionTypeDTO(**asdict(event)), uow)


def on_institution_type_deleted(
    event: 'InstitutionTypeDeleted',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.delete_institution_type(domain.InstitutionTypeDTO(**asdict(event)), uow)
