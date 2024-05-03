from typing import (
    TYPE_CHECKING,
)

from edulib.core.lib_authors.adapters.db import (
    repository,
)
from edulib.core.lib_authors.domain.factories import (
    factory,
)
from edulib.core.utils.tools import (
    modify,
)


if TYPE_CHECKING:
    from edulib.core.lib_authors.domain.factories import (
        AuthorDTO,
    )
    from edulib.core.lib_authors.domain.model import (
        Author,
    )


def create_author(data: 'AuthorDTO') -> 'Author':
    """Сервис создания автора."""
    author = factory.create(data)
    repository.add(author)
    assert author.id is not None, author

    return author


def update_author(data: 'AuthorDTO') -> 'Author':
    """Сервис обновления автора."""
    author = repository.get_object_by_id(data.id)
    modify(author, **data.dict(exclude={'id'}))
    repository.update(author)

    return author
