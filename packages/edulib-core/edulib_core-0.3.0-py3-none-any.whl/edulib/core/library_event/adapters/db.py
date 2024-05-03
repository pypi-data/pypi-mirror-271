from typing import (
    Generator,
)

from django.core.exceptions import (
    ObjectDoesNotExist,
)
from django.forms import (
    model_to_dict,
)
from explicit.adapters.db import (
    AbstractRepository,
)
from explicit.domain.model import (
    asdict,
)

from edulib.core.library_event import (
    domain,
    models as db,
)


class EventRepository(AbstractRepository):

    def get_object_by_id(self, identifier: int) -> domain.Event:
        """Получает объект по идентификатору."""
        try:
            db_instance = db.LibraryEvent.objects.get(pk=identifier)
            return self._to_domain(db_instance)
        except ObjectDoesNotExist as e:
            raise domain.EventNotFound() from e

    def add(self, obj: domain.Event) -> domain.Event:
        assert isinstance(obj, domain.Event)

        return self._to_db(obj)

    def update(self, obj: domain.Event) -> domain.Event:
        assert isinstance(obj, domain.Event)

        return self._to_db(obj)

    def delete(self, obj: domain.Event) -> None:
        assert isinstance(obj, domain.Event)
        db.LibraryEvent.objects.get(pk=obj.id).delete()

    def get_all_objects(self) -> Generator[domain.Event, None, None]:
        for example_type in db.LibraryEvent.objects.iterator():
            yield self._to_domain(example_type)

    def _to_db(self, modelinstance: domain.Event) -> domain.Event:
        assert isinstance(modelinstance, domain.Event)

        db_instance, _ = db.LibraryEvent.objects.update_or_create(
            pk=modelinstance.id,
            defaults=asdict(modelinstance),
        )

        return self.get_object_by_id(db_instance.pk)

    def _to_domain(self, dbinstance: db.LibraryEvent) -> domain.Event:
        return domain.Event(
            library_id=dbinstance.library_id,
            **model_to_dict(dbinstance, exclude=['library']),
        )


repository = EventRepository()
