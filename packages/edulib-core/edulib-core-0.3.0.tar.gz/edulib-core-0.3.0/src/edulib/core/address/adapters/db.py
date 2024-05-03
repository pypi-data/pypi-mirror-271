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

    _domain_model_cls = domain.Address

    @property
    def _base_qs(self) -> 'QuerySet[db.Address]':
        return db.Address.objects.all()

    @property
    def _base_qs_with_deleted(self) -> 'QuerySet[db.Address]':
        return db.Address.objects.all()

    def get_all_objects(self) -> Generator[domain.Address, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.iterator())

    def add(self, address: domain.Address) -> domain.Address:
        assert isinstance(address, domain.Address)
        return self._to_db(address)

    def update(self, address: domain.Address) -> domain.Address:
        assert isinstance(address, domain.Address)
        return self._to_db(address)

    def delete(self, address: domain.Address):
        self._base_qs.filter(id=address.id).delete()

    def _to_db(self, address: domain.Address) -> domain.Address:
        assert isinstance(address, domain.Address)

        db_instance, _ = self._base_qs.update_or_create(
            pk=address.id, defaults=asdict(address)
        )
        address.id = db_instance.pk
        assert address.id is not None

        return address

    def _to_domain(self, dbinstance: 'db.Address') -> domain.Address:
        address = domain.Address(**model_to_dict(dbinstance))

        return address

    def get_object_by_id(self, identifier: int) -> domain.Address:
        try:
            return self._to_domain(self._base_qs.get(pk=identifier))
        except ObjectDoesNotExist as e:
            raise domain.AddressNotFound() from e

    def get_objects_by_ids(self, identifiers: Iterable[int]) -> Generator[domain.Address, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.filter(id__in=identifiers).iterator())


repository = Repository()
