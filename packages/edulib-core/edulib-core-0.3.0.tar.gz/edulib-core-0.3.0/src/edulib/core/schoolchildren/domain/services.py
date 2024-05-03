from typing import (
    TYPE_CHECKING,
)

from .factories import (
    SchoolchildDTO,
    factory,
)
from .model import (
    SchoolchildNotFound,
)


if TYPE_CHECKING:
    from edulib.core.persons.domain.model import (
        Person,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from .model import (
        Schoolchild,
    )


def create_schoolchild(data: 'SchoolchildDTO', uow: 'UnitOfWork') -> 'Schoolchild':
    schoolchild = factory.create(data)
    uow.schoolchildren.add(schoolchild)
    assert schoolchild.id is not None, schoolchild
    return schoolchild


def delete_schoolchild(data: 'SchoolchildDTO', uow: 'UnitOfWork'):
    schoolchild = uow.schoolchildren.get_by_external_id(data.external_id)
    return uow.schoolchilds.delete(schoolchild)


def get_or_create_schoolchild(person: 'Person', uow: 'UnitOfWork'):
    try:
        return uow.schoolchildren.get_by_person_id(person.id)
    except SchoolchildNotFound:
        return create_schoolchild(SchoolchildDTO(person_id=person.id), uow)
