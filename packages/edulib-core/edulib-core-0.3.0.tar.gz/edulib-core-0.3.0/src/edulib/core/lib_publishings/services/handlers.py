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

from edulib.core.lib_publishings.domain import (
    services,
)
from edulib.core.lib_publishings.domain.factories import (
    PublishingDTO,
)
from edulib.core.lib_publishings.services.validators import (
    validate_publishing_name,
)


if TYPE_CHECKING:
    from edulib.core.lib_publishings.domain.commands import (
        CreatePublishing,
        DeletePublishing,
        UpdatePublishing,
    )
    from edulib.core.lib_publishings.domain.model import (
        Publishing,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def create_publishing(
    command: 'CreatePublishing',
    uow: 'UnitOfWork',
) -> 'Publishing':
    with uow.wrap():
        publishing = PublishingDTO(**asdict(command))

        errors = init_messages_dict()
        validate_publishing_name(publishing, errors, uow)
        if errors:
            raise DomainValidationError(errors)

        return services.create_publishing(publishing, uow)


def update_publishing(
    command: 'UpdatePublishing',
    uow: 'UnitOfWork',
) -> 'Publishing':
    with uow.wrap():
        publishing = PublishingDTO(**asdict(command))

        errors = init_messages_dict()
        validate_publishing_name(publishing, errors, uow)
        if errors:
            raise DomainValidationError(errors)

        return services.update_publishing(publishing, uow)


def delete_publishing(
    command: 'DeletePublishing',
    uow: 'UnitOfWork',
) -> None:
    services.delete_publishing(PublishingDTO(**asdict(command)), uow)
