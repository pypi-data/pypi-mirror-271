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
    from edulib.core.academic_years.domain import (
        AcademicYearCreated,
        AcademicYearDeleted,
        AcademicYearUpdated,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def on_academic_year_created(
    event: 'AcademicYearCreated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.create_academic_year(domain.AcademicYearDTO(**asdict(event)), uow)


def on_academic_year_updated(
    event: 'AcademicYearUpdated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.update_academic_year(domain.AcademicYearDTO(**asdict(event)), uow)


def on_academic_year_deleted(
    event: 'AcademicYearDeleted',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.delete_academic_year(domain.AcademicYearDTO(**asdict(event)), uow)
