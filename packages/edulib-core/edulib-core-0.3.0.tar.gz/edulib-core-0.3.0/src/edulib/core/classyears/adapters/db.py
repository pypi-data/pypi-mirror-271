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
    from dataclasses import dataclass  # noqa

    from django.db.models.query import QuerySet  # noqa


class Repository(AbstractRepository):

    _domain_model_cls = domain.ClassYear

    @property
    def _base_qs(self) -> 'QuerySet[db.ClassYear]':
        return db.ClassYear.objects.all()

    @property
    def _base_qs_with_deleted(self) -> 'QuerySet[db.ClassYear]':
        return db.ClassYear.objects.all()

    def get_all_objects(self) -> Generator[domain.ClassYear, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.iterator())

    def add(self, classyear: domain.ClassYear) -> domain.ClassYear:
        assert isinstance(classyear, domain.ClassYear)
        return self._to_db(classyear)

    def update(self, classyear: domain.ClassYear) -> domain.ClassYear:
        assert isinstance(classyear, domain.ClassYear)
        return self._to_db(classyear)

    def delete(self, classyear: domain.ClassYear):
        self._base_qs.filter(id=classyear.id).delete()

    def _to_db(self, classyear: domain.ClassYear) -> domain.ClassYear:
        assert isinstance(classyear, domain.ClassYear)

        db_instance, _ = self._base_qs.update_or_create(
            pk=classyear.id, defaults=asdict(classyear)
        )
        classyear.id = db_instance.pk
        assert classyear.id is not None

        return classyear

    def _to_domain(self, dbinstance: 'db.ClassYear') -> domain.ClassYear:
        classyear = domain.ClassYear(**model_to_dict(dbinstance))
        return classyear

    def get_object_by_id(self, identifier: int) -> domain.ClassYear:
        try:
            return self._to_domain(self._base_qs.get(pk=identifier))
        except ObjectDoesNotExist as e:
            raise domain.ClassYearNotFound() from e

    def get_by_external_id(self, external_id: str) -> domain.ClassYear:
        try:
            return self._to_domain(self._base_qs.get(external_id=external_id))
        except ObjectDoesNotExist as e:
            raise domain.ClassYearNotFound() from e

    def get_objects_by_ids(self, identifiers: Iterable[int]) -> Generator[domain.ClassYear, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.filter(id__in=identifiers).iterator())


repository = Repository()
