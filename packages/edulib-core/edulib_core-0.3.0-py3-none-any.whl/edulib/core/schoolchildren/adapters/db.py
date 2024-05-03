from typing import (
    TYPE_CHECKING,
    Generator,
    Iterable,
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

from .. import (
    domain,
    models as db,
)


if TYPE_CHECKING:
    from dataclasses import (
        dataclass,
    )

    from django.db.models.query import (
        QuerySet,
    )


class Repository(AbstractRepository):

    _domain_model_cls = domain.Schoolchild

    @property
    def _base_qs(self) -> 'QuerySet[db.Schoolchild]':
        return db.Schoolchild.objects.all()

    def get_all_objects(self) -> Generator[domain.Schoolchild, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.iterator())

    def get_object_by_id(self, identifier: int) -> domain.Schoolchild:
        try:
            return self._to_domain(self._base_qs.get(pk=identifier))
        except ObjectDoesNotExist as e:
            raise domain.SchoolchildNotFound() from e

    def get_objects_by_ids(self, identifiers: Iterable[int]) -> Generator[domain.Schoolchild, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.filter(id__in=identifiers).iterator())

    def get_by_person_id(self, person_id: int):
        try:
            return self._to_domain(self._base_qs.get(person_id=person_id))
        except ObjectDoesNotExist as e:
            raise domain.SchoolchildNotFound() from e

    def add(self, schoolchild: domain.Schoolchild) -> domain.Schoolchild:
        assert isinstance(schoolchild, domain.Schoolchild)
        return self._to_db(schoolchild)

    def update(self, schoolchild: domain.Schoolchild) -> domain.Schoolchild:
        assert isinstance(schoolchild, domain.Schoolchild)
        return self._to_db(schoolchild)

    def delete(self, schoolchild: domain.Schoolchild):
        self._base_qs.filter(id=schoolchild.id).delete()

    def _to_db(self, schoolchild: domain.Schoolchild) -> domain.Schoolchild:
        assert isinstance(schoolchild, domain.Schoolchild)

        db_instance, _ = self._base_qs.update_or_create(
            pk=schoolchild.id, defaults=asdict(schoolchild)
        )
        schoolchild.id = db_instance.pk
        assert schoolchild.id is not None

        return schoolchild

    def _to_domain(self, dbinstance: 'db.Schoolchild') -> domain.Schoolchild:
        return domain.Schoolchild(**model_to_dict(dbinstance))


repository = Repository()
