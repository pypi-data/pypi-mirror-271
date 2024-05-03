from typing import (
    TYPE_CHECKING,
)

from explicit.domain.validation.exceptions import (
    DomainValidationError,
    init_messages_dict,
)

from edulib.core.lib_authors.domain import (
    services,
)
from edulib.core.lib_authors.domain.factories import (
    AuthorDTO,
)
from edulib.core.lib_authors.services.validators import (
    validate_author_name,
)


if TYPE_CHECKING:
    from edulib.core.lib_authors.domain.commands import (
        CreateAuthor,
        DeleteAuthor,
        UpdateAuthor,
    )
    from edulib.core.lib_authors.domain.model import (
        Author,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def create_author(
    command: 'CreateAuthor',
    uow: 'UnitOfWork',
) -> 'Author':
    with uow.wrap():
        author = AuthorDTO(**command.dict())

        errors = init_messages_dict()
        validate_author_name(author, errors, uow)
        if errors:
            raise DomainValidationError(errors)

        return services.create_author(author)


def update_author(
    command: 'UpdateAuthor',
    uow: 'UnitOfWork',
) -> 'Author':
    with uow.wrap():
        author = AuthorDTO(**command.dict())

        errors = init_messages_dict()
        validate_author_name(author, errors, uow)
        if errors:
            raise DomainValidationError(errors)

        return services.update_author(author)


def delete_author(
    command: 'DeleteAuthor',
    uow: 'UnitOfWork',
) -> None:
    author = uow.authors.get_object_by_id(command.id)
    uow.authors.delete(author)
