from dataclasses import (
    asdict,
)
from typing import (
    Generator,
)

from django.core.exceptions import (
    ObjectDoesNotExist,
)
from explicit.adapters.db import (
    AbstractRepository,
)

from edulib.core.lib_sources import (
    models as db,
)
from edulib.core.lib_sources.domain.model import (
    Source,
    SourceNotFound,
)


class SourceRepository(AbstractRepository):

    def get_object_by_id(self, identifier: int) -> Source:
        """Получает объект по идентификатору."""
        try:
            db_instance = db.LibrarySource.objects.get(pk=identifier)
            return self._to_domain(db_instance)
        except ObjectDoesNotExist as e:
            raise SourceNotFound() from e

    def add(self, obj: Source) -> Source:
        assert isinstance(obj, Source)
        return self._to_db(obj)

    def update(self, obj: Source) -> Source:
        assert isinstance(obj, Source)
        return self._to_db(obj)

    def delete(self, obj: Source) -> None:
        assert isinstance(obj, Source)
        db.LibrarySource.objects.get(pk=obj.id).delete()

    def get_all_objects(self) -> Generator[Source, None, None]:
        for source in db.LibrarySource.objects.iterator():
            yield self._to_domain(source)

    def source_exists(self, source: Source) -> bool:
        """
        Предикат: существует ли источник поступления с указанным именем
        и принадлежащий определенной организации.
        """
        return (db.LibrarySource.objects
                .exclude(pk=source.id)
                .filter(name__iexact=source.name, school_id=source.school_id)
                .exists())

    def _to_db(self, modelinstance: Source) -> Source:
        assert isinstance(modelinstance, Source)

        db_instance, _ = db.LibrarySource.objects.update_or_create(
            pk=modelinstance.id,
            defaults=asdict(modelinstance),
        )
        modelinstance.id = db_instance.pk

        return modelinstance

    def _to_domain(self, dbinstance: db.LibrarySource) -> Source:
        return Source(
            id=dbinstance.pk,
            name=dbinstance.name,
            school_id=dbinstance.school_id,
        )


repository = SourceRepository()
