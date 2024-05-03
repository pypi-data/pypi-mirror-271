from typing import (
    TYPE_CHECKING,
)

from edulib.core.lib_sources.domain.factories import (
    SourceDTO,
    factory,
)
from edulib.core.lib_sources.domain.model import (
    Source,
)
from edulib.core.utils.tools import (
    modify,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def create_source(data: SourceDTO, uow: 'UnitOfWork') -> 'Source':
    """Сервис создания источника поступления."""
    source = factory.create(data)
    uow.sources.add(source)
    assert source.id is not None, source

    return source


def update_source(data: SourceDTO, uow: 'UnitOfWork') -> 'Source':
    """Сервис обновления источника поступления."""
    source = uow.sources.get_object_by_id(data.id)
    modify(source, **data.dict(exclude={'id'}))
    uow.sources.update(source)

    return source


def delete_source(data: SourceDTO, uow: 'UnitOfWork') -> None:
    """Сервис удаления источника поступления."""
    source = uow.sources.get_object_by_id(data.id)
    uow.sources.delete(source)
