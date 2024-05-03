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

    @property
    def _base_qs(self) -> 'QuerySet[db.Parallel]':
        return db.Parallel.objects.all()

    @property
    def _base_qs_with_deleted(self) -> 'QuerySet[db.Parallel]':
        return db.Parallel.objects.all()

    def get_all_objects(self) -> Generator[domain.Parallel, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.iterator())

    def add(self, parallel: domain.Parallel) -> domain.Parallel:
        assert isinstance(parallel, domain.Parallel)

        return self._to_db(parallel)

    def update(self, parallel: domain.Parallel) -> domain.Parallel:
        assert isinstance(parallel, domain.Parallel)

        return self._to_db(parallel)

    def delete(self, parallel: domain.Parallel):
        self._base_qs.filter(id=parallel.id).delete()

    def _to_db(self, parallel: domain.Parallel) -> domain.Parallel:
        assert isinstance(parallel, domain.Parallel)

        db_instance, _ = self._base_qs.update_or_create(
            pk=parallel.id, defaults=asdict(parallel)
        )
        parallel.id = db_instance.pk
        assert parallel.id is not None

        return parallel

    def _to_domain(self, dbinstance: 'db.Parallel') -> domain.Parallel:
        parallel = domain.Parallel(**model_to_dict(dbinstance))

        return parallel

    def get_object_by_id(self, identifier: int) -> domain.Parallel:
        try:
            return self._to_domain(self._base_qs.get(pk=identifier))
        except ObjectDoesNotExist as e:
            raise domain.ParallelNotFound() from e

    def get_by_external_id(self, external_id: str) -> domain.Parallel:
        try:
            return self._to_domain(self._base_qs.get(external_id=external_id))
        except ObjectDoesNotExist as e:
            raise domain.ParallelNotFound() from e

    def get_objects_by_ids(self, identifiers: Iterable[int]) -> Generator[domain.Parallel, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.filter(id__in=identifiers).iterator())


repository = Repository()
