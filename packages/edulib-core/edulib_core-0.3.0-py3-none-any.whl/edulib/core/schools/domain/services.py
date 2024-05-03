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
        SchoolDTO,
    )
    from .model import (
        School,
    )


def create_school(data: 'SchoolDTO', uow: 'UnitOfWork') -> 'School':
    school = factory.create(data)
    uow.schools.add(school)
    assert school.id is not None, school

    return school


def update_school(data: 'SchoolDTO', uow: 'UnitOfWork') -> 'School':
    school = uow.schools.get_by_external_id(data.external_id)
    modify(school, **data.dict(exclude={'id'}))

    return uow.schools.update(school)


def delete_school(data: 'SchoolDTO', uow: 'UnitOfWork'):
    school = uow.schools.get_by_external_id(data.external_id)

    return uow.schools.delete(school)
