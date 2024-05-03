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
        PersonDTO,
    )
    from .model import (
        Person,
    )


def create_person(data: 'PersonDTO', uow: 'UnitOfWork') -> 'Person':
    person = factory.create(data)
    uow.persons.add(person)
    assert person.id is not None, person
    return person


def update_person(data: 'PersonDTO', uow: 'UnitOfWork'):
    person = uow.persons.get_by_external_id(data.external_id)
    modify(person, **data.dict(exclude={'id'}))
    return uow.persons.update(person)


def delete_person(data: 'PersonDTO', uow: 'UnitOfWork'):
    person = uow.persons.get_by_external_id(data.external_id)
    return uow.persons.delete(person)
