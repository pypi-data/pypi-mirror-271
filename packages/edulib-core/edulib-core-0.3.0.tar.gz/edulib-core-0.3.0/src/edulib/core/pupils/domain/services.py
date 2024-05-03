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
        PupilDTO,
    )
    from .model import (
        Pupil,
    )


def create_pupil(data: 'PupilDTO', uow: 'UnitOfWork') -> 'Pupil':
    pupil = factory.create(data)
    uow.pupils.add(pupil)
    assert pupil.id is not None, pupil
    return pupil


def update_pupil(data: 'PupilDTO', uow: 'UnitOfWork'):
    pupil = uow.pupils.get_by_external_id(data.external_id)
    modify(pupil, **data.dict(exclude={'id'}))
    return uow.pupils.update(pupil)


def delete_pupil(data: 'PupilDTO', uow: 'UnitOfWork'):
    pupil = uow.pupils.get_by_external_id(data.external_id)
    return uow.pupils.delete(pupil)
