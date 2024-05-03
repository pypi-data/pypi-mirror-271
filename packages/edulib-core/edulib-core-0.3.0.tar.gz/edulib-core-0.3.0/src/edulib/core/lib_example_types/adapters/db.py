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

from edulib.core.lib_example_types import (
    models as db,
)
from edulib.core.lib_example_types.domain.model import (
    ExampleType,
    ExampleTypeNotFound,
)


class Repository(AbstractRepository):

    def get_object_by_id(self, identifier: int) -> ExampleType:
        """Получает объект по идентификатору."""
        try:
            db_instance = db.LibraryExampleType.objects.get(pk=identifier)
            return self._to_domain(db_instance)
        except ObjectDoesNotExist as e:
            raise ExampleTypeNotFound() from e

    def add(self, obj: ExampleType) -> ExampleType:
        assert isinstance(obj, ExampleType)

        return self._to_db(obj)

    def update(self, obj: ExampleType) -> ExampleType:
        assert isinstance(obj, ExampleType)

        return self._to_db(obj)

    def delete(self, obj: ExampleType) -> None:
        assert isinstance(obj, ExampleType)
        db.LibraryExampleType.objects.filter(pk=obj.id).delete()

    def get_all_objects(self) -> Generator[ExampleType, None, None]:
        for example_type in db.LibraryExampleType.objects.iterator():
            yield self._to_domain(example_type)

    def is_exists(self, example_type: ExampleType) -> bool:
        """Проверят существование типа библиотечных экземпляров с таким же именем."""
        return db.LibraryExampleType.objects.exclude(pk=example_type.id).filter(
            name__iexact=example_type.name,
        ).exists()

    def _to_db(self, modelinstance: ExampleType) -> ExampleType:
        assert isinstance(modelinstance, ExampleType)

        db_instance, _ = db.LibraryExampleType.objects.update_or_create(
            pk=modelinstance.id,
            defaults=asdict(modelinstance),
        )
        modelinstance.id = db_instance.pk

        return modelinstance

    def _to_domain(self, dbinstance: db.LibraryExampleType) -> ExampleType:
        return ExampleType(**model_to_dict(dbinstance))


repository = Repository()
