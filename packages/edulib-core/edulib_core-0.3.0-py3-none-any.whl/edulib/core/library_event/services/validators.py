from typing import (
    TYPE_CHECKING,
    Mapping,
)

from edulib.core.lib_passport.domain.model import (
    PassportNotFound,
)
from edulib.core.library_event import (
    domain,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def validate_event(data: domain.EventDTO, errors: Mapping[str, list[str]], uow: 'UnitOfWork') -> None:
    """Валидация плана работы библиотеки."""
    if data.library_id:
        try:
            uow.passports.get_by_id(data.library_id)
        except PassportNotFound as exc:
            errors['library_id'].append(str(exc))
