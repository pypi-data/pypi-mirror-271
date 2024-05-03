from typing import (
    TYPE_CHECKING,
)

from explicit.domain.model import (
    asdict,
)
from explicit.domain.validation.exceptions import (
    DomainValidationError,
    init_messages_dict,
)

from edulib.core.lib_sources.domain import (
    services,
)
from edulib.core.lib_sources.domain.factories import (
    SourceDTO,
)
from edulib.core.lib_sources.services.validators import (
    validate_source_name,
)


if TYPE_CHECKING:
    from edulib.core.lib_sources.domain.commands import (
        CreateSource,
        DeleteSource,
        UpdateSource,
    )
    from edulib.core.lib_sources.domain.model import (
        Source,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def create_source(
    command: 'CreateSource',
    uow: 'UnitOfWork',
) -> 'Source':
    with uow.wrap():
        source = SourceDTO(**asdict(command))

        errors = init_messages_dict()
        validate_source_name(source, errors, uow)
        if errors:
            raise DomainValidationError(errors)
        return services.create_source(source, uow)


def update_source(
    command: 'UpdateSource',
    uow: 'UnitOfWork',
) -> 'Source':
    with uow.wrap():
        source = SourceDTO(**asdict(command))
        obj = uow.sources.get_object_by_id(command.id)

        errors = init_messages_dict()
        validate_source_name(source, errors, uow, obj=obj)
        if errors:
            raise DomainValidationError(errors)

        return services.update_source(source, uow)


def delete_source(
    command: 'DeleteSource',
    uow: 'UnitOfWork',
) -> None:
    services.delete_source(SourceDTO(**asdict(command)), uow)
