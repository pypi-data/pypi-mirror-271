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
    def _base_qs(self) -> 'QuerySet[db.InstitutionType]':
        return db.InstitutionType.objects.all()

    @property
    def _base_qs_with_deleted(self) -> 'QuerySet[db.InstitutionType]':
        return db.InstitutionType.objects.all()

    def get_all_objects(self) -> Generator[domain.InstitutionType, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.iterator())

    def add(self, institution_type: domain.InstitutionType) -> domain.InstitutionType:
        assert isinstance(institution_type, domain.InstitutionType)

        return self._to_db(institution_type)

    def update(self, institution_type: domain.InstitutionType) -> domain.InstitutionType:
        assert isinstance(institution_type, domain.InstitutionType)

        return self._to_db(institution_type)

    def delete(self, institution_type: domain.InstitutionType):
        self._base_qs.filter(id=institution_type.id).delete()

    def _to_db(self, institution_type: domain.InstitutionType) -> domain.InstitutionType:
        assert isinstance(institution_type, domain.InstitutionType)

        db_instance, _ = self._base_qs.update_or_create(
            pk=institution_type.id, defaults=asdict(institution_type)
        )
        institution_type.id = db_instance.pk
        assert institution_type.id is not None

        return institution_type

    def _to_domain(self, dbinstance: 'db.InstitutionType') -> domain.InstitutionType:
        institution_type = domain.InstitutionType(**model_to_dict(dbinstance))

        return institution_type

    def get_object_by_id(self, identifier: int) -> domain.InstitutionType:
        try:
            return self._to_domain(self._base_qs.get(pk=identifier))
        except ObjectDoesNotExist as e:
            raise domain.InstitutionTypeNotFound() from e

    def get_by_external_id(self, external_id: str) -> domain.InstitutionType:
        try:
            return self._to_domain(self._base_qs.get(external_id=external_id))
        except ObjectDoesNotExist as e:
            raise domain.InstitutionTypeNotFound() from e

    def get_objects_by_ids(self, identifiers: Iterable[int]) -> Generator[domain.InstitutionType, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.filter(id__in=identifiers).iterator())


repository = Repository()
