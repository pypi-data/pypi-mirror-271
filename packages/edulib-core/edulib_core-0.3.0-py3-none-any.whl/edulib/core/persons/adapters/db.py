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

    _domain_model_cls = domain.Person

    @property
    def _base_qs(self) -> 'QuerySet[db.Person]':
        return db.Person.objects.all()

    @property
    def _base_qs_with_deleted(self) -> 'QuerySet[db.Person]':
        return db.Person.objects.all()

    def get_all_objects(self) -> Generator[domain.Person, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.iterator())

    def add(self, person: domain.Person) -> domain.Person:
        assert isinstance(person, domain.Person)
        return self._to_db(person)

    def update(self, person: domain.Person) -> domain.Person:
        assert isinstance(person, domain.Person)
        return self._to_db(person)

    def delete(self, person: domain.Person):
        self._base_qs.filter(id=person.id).delete()

    def _to_db(self, person: domain.Person) -> domain.Person:
        assert isinstance(person, domain.Person)

        db_instance, _ = self._base_qs.update_or_create(
            pk=person.id, defaults=asdict(person)
        )
        person.id = db_instance.pk
        assert person.id is not None

        return person

    def _to_domain(self, dbinstance: 'db.Person') -> domain.Person:
        person = domain.Person(**model_to_dict(dbinstance))
        return person

    def get_object_by_id(self, identifier: int) -> domain.Person:
        try:
            return self._to_domain(self._base_qs.get(pk=identifier))
        except ObjectDoesNotExist as e:
            raise domain.PersonNotFound() from e

    def get_by_external_id(self, external_id: str) -> domain.Person:
        try:
            return self._to_domain(self._base_qs.get(external_id=external_id))
        except ObjectDoesNotExist as e:
            raise domain.PersonNotFound() from e

    def get_objects_by_ids(self, identifiers: Iterable[int]) -> Generator[domain.Person, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.filter(id__in=identifiers).iterator())


repository = Repository()
