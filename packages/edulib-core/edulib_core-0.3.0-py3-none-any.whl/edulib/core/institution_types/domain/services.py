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
        InstitutionTypeDTO,
    )
    from .model import (
        InstitutionType,
    )


def create_institution_type(data: 'InstitutionTypeDTO', uow: 'UnitOfWork') -> 'InstitutionType':
    institution_type = factory.create(data)
    uow.institution_types.add(institution_type)
    assert institution_type.id is not None, institution_type

    return institution_type


def update_institution_type(data: 'InstitutionTypeDTO', uow: 'UnitOfWork') -> 'InstitutionType':
    institution_type = uow.institution_types.get_by_external_id(data.external_id)
    modify(institution_type, **data.dict(exclude={'id'}))
    return uow.institution_types.update(institution_type)


def delete_institution_type(data: 'InstitutionTypeDTO', uow: 'UnitOfWork'):
    institution_type = uow.institution_types.get_by_external_id(data.external_id)

    return uow.institution_types.delete(institution_type)
