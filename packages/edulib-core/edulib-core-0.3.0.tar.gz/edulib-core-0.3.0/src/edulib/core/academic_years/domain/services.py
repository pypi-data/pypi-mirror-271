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
        AcademicYearDTO,
    )
    from .model import (
        AcademicYear,
    )


def create_academic_year(data: 'AcademicYearDTO', uow: 'UnitOfWork') -> 'AcademicYear':
    academic_year = factory.create(data)
    uow.academic_years.add(academic_year)
    assert academic_year.id is not None, academic_year

    return academic_year


def update_academic_year(data: 'AcademicYearDTO', uow: 'UnitOfWork') -> 'AcademicYear':
    academic_year = uow.academic_years.get_by_external_id(data.external_id)
    modify(academic_year, **data.dict(exclude={'id'}))

    return uow.academic_years.update(academic_year)


def delete_academic_year(data: 'AcademicYearDTO', uow: 'UnitOfWork'):
    academic_year = uow.academic_years.get_by_external_id(data.external_id)

    return uow.academic_years.delete(academic_year)
