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
    def _base_qs(self) -> 'QuerySet[db.MunicipalUnit]':
        return db.MunicipalUnit.objects.all()

    def get_all_objects(self) -> Generator[domain.MunicipalUnit, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.iterator())

    def add(self, municipal_unit: domain.MunicipalUnit) -> domain.MunicipalUnit:
        assert isinstance(municipal_unit, domain.MunicipalUnit)

        return self._to_db(municipal_unit)

    def update(self, municipal_unit: domain.MunicipalUnit) -> domain.MunicipalUnit:
        assert isinstance(municipal_unit, domain.MunicipalUnit)

        return self._to_db(municipal_unit)

    def delete(self, municipal_unit: domain.MunicipalUnit):
        self._base_qs.filter(id=municipal_unit.id).delete()

    def _to_db(self, municipal_unit: domain.MunicipalUnit) -> domain.MunicipalUnit:
        assert isinstance(municipal_unit, domain.MunicipalUnit)

        db_instance, _ = self._base_qs.update_or_create(
            pk=municipal_unit.id, defaults=asdict(
                municipal_unit, exclude={'parent'}
            ) | {
                'parent_id': municipal_unit.parent.id if municipal_unit.parent else None,
            }
        )
        municipal_unit.id = db_instance.pk
        assert municipal_unit.id is not None

        return municipal_unit

    def _to_domain(self, dbinstance: 'db.MunicipalUnit') -> domain.MunicipalUnit:
        params = model_to_dict(dbinstance, exclude=['parent'])

        municipal_unit = domain.MunicipalUnit(**params | {
            'parent': self._to_domain(dbinstance.parent) if dbinstance.parent else None,
        })

        return municipal_unit

    def get_object_by_id(self, identifier: int) -> domain.MunicipalUnit:
        try:
            return self._to_domain(self._base_qs.get(pk=identifier))
        except ObjectDoesNotExist as e:
            raise domain.MunicipalUnitNotFound() from e

    def get_by_external_id(self, external_id: str) -> domain.MunicipalUnit:
        try:
            return self._to_domain(self._base_qs.get(external_id=external_id))
        except ObjectDoesNotExist as e:
            raise domain.MunicipalUnitNotFound() from e

    def get_objects_by_ids(self, identifiers: Iterable[int]) -> Generator[domain.MunicipalUnit, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.filter(id__in=identifiers).iterator())


repository = Repository()
