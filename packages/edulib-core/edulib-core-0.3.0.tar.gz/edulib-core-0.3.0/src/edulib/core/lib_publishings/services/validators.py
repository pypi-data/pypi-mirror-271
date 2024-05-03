from typing import (
    TYPE_CHECKING,
    Mapping,
)

from edulib.core.lib_publishings.domain.factories import (
    PublishingDTO,
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def validate_publishing_name(data: PublishingDTO, errors: Mapping[str, list[str]], uow: 'UnitOfWork') -> None:
    """Валидация наименования издательства."""
    name = data.name.strip()
    if name:
        publishing = factory.create(data)
        if uow.publishings.publishing_exists(publishing):
            errors['name'].append('Такое издательство уже существует')
    else:
        errors['name'].append('Наименование не может быть пустым')
