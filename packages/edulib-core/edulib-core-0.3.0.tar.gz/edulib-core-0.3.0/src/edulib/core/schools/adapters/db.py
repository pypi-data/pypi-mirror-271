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
    def _base_qs(self) -> 'QuerySet[db.School]':
        return db.School.objects.all()

    def get_all_objects(self) -> Generator[domain.School, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.iterator())

    def add(self, school: domain.School) -> domain.School:
        assert isinstance(school, domain.School)

        return self._to_db(school)

    def update(self, school: domain.School) -> domain.School:
        assert isinstance(school, domain.School)

        return self._to_db(school)

    def delete(self, school: domain.School):
        self._base_qs.filter(id=school.id).delete()

    def _to_db(self, school: domain.School) -> domain.School:
        assert isinstance(school, domain.School)

        db_instance, _ = self._base_qs.update_or_create(
            pk=school.id, defaults=asdict(
                school, exclude={'parent'}
            ) | {
                'parent_id': school.parent.id if school.parent else None
            }
        )
        school.id = db_instance.pk
        assert school.id is not None

        return school

    def _to_domain(self, dbinstance: 'db.School') -> domain.School:
        params = model_to_dict(dbinstance, exclude=['parent'])

        school = domain.School(**params | {
            'parent': self._to_domain(dbinstance.parent) if dbinstance.parent else None
        })

        return school

    def get_object_by_id(self, identifier: int) -> domain.School:
        try:
            return self._to_domain(self._base_qs.get(pk=identifier))
        except ObjectDoesNotExist as e:
            raise domain.SchoolNotFound() from e

    def get_by_external_id(self, external_id: str) -> domain.School:
        try:
            return self._to_domain(self._base_qs.get(external_id=external_id))
        except ObjectDoesNotExist as e:
            raise domain.SchoolNotFound() from e

    def get_objects_by_ids(self, identifiers: Iterable[int]) -> Generator[domain.School, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.filter(id__in=identifiers).iterator())


repository = Repository()
