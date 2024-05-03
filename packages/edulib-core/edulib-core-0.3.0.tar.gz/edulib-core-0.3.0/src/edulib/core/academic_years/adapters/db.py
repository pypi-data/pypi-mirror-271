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
    def _base_qs(self) -> 'QuerySet[db.AcademicYear]':
        return db.AcademicYear.objects.all()

    @property
    def _base_qs_with_deleted(self) -> 'QuerySet[db.AcademicYear]':
        return db.AcademicYear.objects.all()

    def get_all_objects(self) -> Generator[domain.AcademicYear, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.iterator())

    def add(self, academic_year: domain.AcademicYear) -> domain.AcademicYear:
        assert isinstance(academic_year, domain.AcademicYear)

        return self._to_db(academic_year)

    def update(self, academic_year: domain.AcademicYear) -> domain.AcademicYear:
        assert isinstance(academic_year, domain.AcademicYear)

        return self._to_db(academic_year)

    def delete(self, academic_year: domain.AcademicYear):
        self._base_qs.filter(id=academic_year.id).delete()

    def _to_db(self, academic_year: domain.AcademicYear) -> domain.AcademicYear:
        assert isinstance(academic_year, domain.AcademicYear)

        db_instance, _ = self._base_qs.update_or_create(
            pk=academic_year.id, defaults=asdict(academic_year)
        )
        academic_year.id = db_instance.pk
        assert academic_year.id is not None

        return academic_year

    def _to_domain(self, dbinstance: 'db.AcademicYear') -> domain.AcademicYear:
        academic_year = domain.AcademicYear(**model_to_dict(dbinstance))

        return academic_year

    def get_object_by_id(self, identifier: int) -> domain.AcademicYear:
        try:
            return self._to_domain(self._base_qs.get(pk=identifier))
        except ObjectDoesNotExist as e:
            raise domain.AcademicYearNotFound() from e

    def get_by_external_id(self, external_id: str) -> domain.AcademicYear:
        try:
            return self._to_domain(self._base_qs.get(external_id=external_id))
        except ObjectDoesNotExist as e:
            raise domain.AcademicYearNotFound() from e

    def get_objects_by_ids(self, identifiers: Iterable[int]) -> Generator[domain.AcademicYear, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.filter(id__in=identifiers).iterator())


repository = Repository()
