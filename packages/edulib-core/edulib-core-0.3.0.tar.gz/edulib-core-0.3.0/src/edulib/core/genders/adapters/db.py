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
    def _base_qs(self) -> 'QuerySet[db.Gender]':
        return db.Gender.objects.all()

    @property
    def _base_qs_with_deleted(self) -> 'QuerySet[db.Gender]':
        return db.Gender.objects.all()

    def get_all_objects(self) -> Generator[domain.Gender, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.iterator())

    def add(self, gender: domain.Gender) -> domain.Gender:
        assert isinstance(gender, domain.Gender)

        return self._to_db(gender)

    def update(self, gender: domain.Gender) -> domain.Gender:
        assert isinstance(gender, domain.Gender)

        return self._to_db(gender)

    def delete(self, gender: domain.Gender):
        self._base_qs.filter(id=gender.id).delete()

    def _to_db(self, gender: domain.Gender) -> domain.Gender:
        assert isinstance(gender, domain.Gender)

        db_instance, _ = self._base_qs.update_or_create(
            pk=gender.id, defaults=asdict(gender)
        )
        gender.id = db_instance.pk
        assert gender.id is not None

        return gender

    def _to_domain(self, dbinstance: 'db.Gender') -> domain.Gender:
        gender = domain.Gender(**model_to_dict(dbinstance))

        return gender

    def get_object_by_id(self, identifier: int) -> domain.Gender:
        try:
            return self._to_domain(self._base_qs.get(pk=identifier))
        except ObjectDoesNotExist as e:
            raise domain.GenderNotFound() from e

    def get_by_external_id(self, external_id: str) -> domain.Gender:
        try:
            return self._to_domain(self._base_qs.get(external_id=external_id))
        except ObjectDoesNotExist as e:
            raise domain.GenderNotFound() from e

    def get_objects_by_ids(self, identifiers: Iterable[int]) -> Generator[domain.Gender, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.filter(id__in=identifiers).iterator())


repository = Repository()
