from django.core.exceptions import (
    ValidationError,
)

from edulib.core.lib_authors.models import (
    LibraryAuthors,
)
from edulib.core.lib_registry.adapters.db import (
    registry_entries,
)


def save_registry_entry(entry, school_id, authors_ids, study_level_ids):
    # проверяем, нет ли похожих карточек
    if not registry_entries.is_unique_in_school(entry, school_id, authors_ids):
        raise ValidationError(
            'Такая карточка учета экземпляра уже существует'
        )

    # обновляется текстовое поле отображения Авторов
    # используется в прочих реестрах библиотеки
    entry.authors = ', '.join(
        LibraryAuthors.objects.filter(
            id__in=authors_ids
        ).values_list('name', flat=True)
    ) or '-'

    # сначала сохраняем экземпляр
    entry.save()

    # только потом - связанные записи
    entry.study_levels.set(study_level_ids)

    # Сохраняем авторов
    entry.libauthorsregentries_set.all().delete()
    for author_id in authors_ids:
        entry.libauthorsregentries_set.create(author_id=author_id)
