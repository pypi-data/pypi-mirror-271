from typing import (
    Generator,
)

from django.core.exceptions import (
    ObjectDoesNotExist,
)
from explicit.adapters.db import (
    AbstractRepository,
)
from explicit.domain import (
    asdict,
)

from edulib.core.lib_publishings import (
    models as db,
)
from edulib.core.lib_publishings.domain.model import (
    Publishing,
    PublishingNotFound,
)


class PublishingRepository(AbstractRepository):

    def get_object_by_id(self, identifier: int) -> Publishing:
        """Получает объект по идентификатору."""
        try:
            db_instance = db.LibraryPublishings.objects.get(pk=identifier)
            return self._to_domain(db_instance)
        except ObjectDoesNotExist as e:
            raise PublishingNotFound() from e

    def add(self, obj: Publishing) -> Publishing:
        assert isinstance(obj, Publishing)

        return self._to_db(obj)

    def update(self, obj: Publishing) -> Publishing:
        assert isinstance(obj, Publishing)

        return self._to_db(obj)

    def delete(self, obj: Publishing) -> None:
        assert isinstance(obj, Publishing)
        db.LibraryPublishings.objects.get(pk=obj.id).delete()

    def get_all_objects(self) -> Generator[Publishing, None, None]:
        for publishing in db.LibraryPublishings.objects.iterator():
            yield self._to_domain(publishing)

    def publishing_exists(self, publishing: Publishing) -> bool:
        """Проверяет существование издательства с таким же именем."""
        return db.LibraryPublishings.objects.exclude(pk=publishing.id).filter(
            name__iexact=publishing.name,
        ).exists()

    def _to_db(self, modelinstance: Publishing) -> Publishing:
        assert isinstance(modelinstance, Publishing)

        db_instance, _ = db.LibraryPublishings.objects.update_or_create(
            pk=modelinstance.id,
            defaults=asdict(modelinstance),
        )
        modelinstance.id = db_instance.pk

        return modelinstance

    def _to_domain(self, dbinstance: db.LibraryPublishings) -> Publishing:
        return Publishing(
            id=dbinstance.pk,
            name=dbinstance.name,
        )


repository = PublishingRepository()
