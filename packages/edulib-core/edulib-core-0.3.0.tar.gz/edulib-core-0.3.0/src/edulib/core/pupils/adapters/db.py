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

    _domain_model_cls = domain.Pupil

    @property
    def _base_qs(self) -> 'QuerySet[db.Pupil]':
        return db.Pupil.objects.all()

    @property
    def _base_qs_with_deleted(self) -> 'QuerySet[db.Pupil]':
        return db.Pupil.objects.all()

    def get_all_objects(self) -> Generator[domain.Pupil, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.iterator())

    def add(self, pupil: domain.Pupil) -> domain.Pupil:
        assert isinstance(pupil, domain.Pupil)
        return self._to_db(pupil)

    def update(self, pupil: domain.Pupil) -> domain.Pupil:
        assert isinstance(pupil, domain.Pupil)
        return self._to_db(pupil)

    def delete(self, pupil: domain.Pupil):
        self._base_qs.filter(id=pupil.id).delete()

    def _to_db(self, pupil: domain.Pupil) -> domain.Pupil:
        assert isinstance(pupil, domain.Pupil)

        db_instance, _ = self._base_qs.update_or_create(
            pk=pupil.id, defaults=asdict(pupil)
        )
        pupil.id = db_instance.pk
        assert pupil.id is not None

        return pupil

    def _to_domain(self, dbinstance: 'db.Pupil') -> domain.Pupil:
        pupil = domain.Pupil(**model_to_dict(dbinstance))
        return pupil

    def get_object_by_id(self, identifier: int) -> domain.Pupil:
        try:
            return self._to_domain(self._base_qs.get(pk=identifier))
        except ObjectDoesNotExist as e:
            raise domain.PupilNotFound() from e

    def get_by_external_id(self, external_id: str) -> domain.Pupil:
        try:
            return self._to_domain(self._base_qs.get(external_id=external_id))
        except ObjectDoesNotExist as e:
            raise domain.PupilNotFound() from e

    def get_objects_by_ids(self, identifiers: Iterable[int]) -> Generator[domain.Pupil, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.filter(id__in=identifiers).iterator())


repository = Repository()
