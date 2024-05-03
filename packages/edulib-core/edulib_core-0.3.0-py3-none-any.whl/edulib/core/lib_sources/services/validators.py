from typing import (
    TYPE_CHECKING,
    Mapping,
)

from edulib.core.lib_sources.domain.factories import (
    SourceDTO,
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def validate_source_name(data: SourceDTO, errors: Mapping[str, list[str]], uow: 'UnitOfWork', obj=None) -> None:
    """Валидация источника поступления."""
    # В случае обновления school_id возьмем из обновляемого объекта
    if obj:
        data = data.copy(update={'school_id': obj.school_id})
    if 'name' in data.dict():
        name = data.name.strip()
        if name:
            source = factory.create(data)
            if uow.sources.source_exists(source):
                errors['name'].append(
                    f'Источник поступления с именем "{name}" уже существует для указанной организации'
                )
        else:
            errors['name'].append('Наименование не может быть пустым')
