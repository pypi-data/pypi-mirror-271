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
        ClassYearDTO,
    )
    from .model import (
        ClassYear,
    )


def create_classyear(data: 'ClassYearDTO', uow: 'UnitOfWork') -> 'ClassYear':
    classyear = factory.create(data)
    uow.classyears.add(classyear)
    assert classyear.id is not None, classyear
    return classyear


def update_classyear(data: 'ClassYearDTO', uow: 'UnitOfWork') -> 'ClassYear':
    classyear = uow.classyears.get_by_external_id(data.external_id)
    modify(classyear, **data.dict(exclude={'id'}))
    return uow.classyears.update(classyear)


def delete_classyear(data: 'ClassYearDTO', uow: 'UnitOfWork'):
    classyear = uow.classyears.get_by_external_id(data.external_id)
    return uow.classyears.delete(classyear)
