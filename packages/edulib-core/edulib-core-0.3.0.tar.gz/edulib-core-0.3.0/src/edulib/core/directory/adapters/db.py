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
from explicit.domain import (
    asdict,
)

from edulib.core.directory import (
    domain,
    models as db,
)


class BbkRepository(AbstractRepository):

    def get_object_by_id(self, identifier: int) -> domain.Bbk:
        """Получает объект по идентификатору."""
        try:
            db_instance = db.Catalog.objects.get(pk=identifier)
            return self._to_domain(db_instance)
        except ObjectDoesNotExist as exc:
            raise domain.BbkNotFound from exc

    def add(self, obj: domain.Bbk) -> domain.Bbk:
        assert isinstance(obj, domain.Bbk)

        return self._to_db(obj)

    def update(self, obj: domain.Bbk) -> domain.Bbk:
        assert isinstance(obj, domain.Bbk)

        return self._to_db(obj)

    def delete(self, obj: domain.Bbk) -> None:
        assert isinstance(obj, domain.Bbk)
        db.Catalog.objects.filter(pk=obj.id).delete()

    def get_all_objects(self) -> Generator[domain.Bbk, None, None]:
        for bbk in db.Catalog.objects.iterator():
            yield self._to_domain(bbk)

    def is_exists(self, bbk: domain.Bbk) -> bool:
        """Проверяет существует ли раздел ББК с указанным кодом."""
        return db.Catalog.objects.exclude(pk=bbk.id).filter(code__iexact=bbk.code).exists()

    def _to_db(self, modelinstance: domain.Bbk) -> domain.Bbk:
        assert isinstance(modelinstance, domain.Bbk)

        db_instance, _ = db.Catalog.objects.update_or_create(
            pk=modelinstance.id,
            defaults=asdict(modelinstance),
        )
        modelinstance.id = db_instance.pk

        return modelinstance

    def _to_domain(self, dbinstance: db.Catalog) -> domain.Bbk:
        return domain.Bbk(
            parent_id=dbinstance.parent_id,
            **model_to_dict(dbinstance, exclude=['parent']),
        )


repository = BbkRepository()
