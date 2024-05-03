from typing import (
    TYPE_CHECKING,
    Mapping,
)

from edulib.core.lib_authors.domain.factories import (
    AuthorDTO,
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def validate_author_name(data: AuthorDTO, errors: Mapping[str, list[str]], uow: 'UnitOfWork') -> None:
    """Валидация наименования автора."""
    author = factory.create(data)
    if uow.authors.author_exists(author):
        errors['name'].append('Такой автор уже существует')
