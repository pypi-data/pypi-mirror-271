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
        GenderDTO,
    )
    from .model import (
        Gender,
    )


def create_gender(data: 'GenderDTO', uow: 'UnitOfWork') -> 'Gender':
    gender = factory.create(data)
    uow.genders.add(gender)
    assert gender.id is not None, gender

    return gender


def update_gender(data: 'GenderDTO', uow: 'UnitOfWork') -> 'Gender':
    gender = uow.genders.get_by_external_id(data.external_id)
    modify(gender, **data.dict(exclude={'id'}))

    return uow.genders.update(gender)


def delete_gender(data: 'GenderDTO', uow: 'UnitOfWork'):
    gender = uow.genders.get_by_external_id(data.external_id)

    return uow.genders.delete(gender)
