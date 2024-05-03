from abc import (
    ABC,
)

from django.db.models import (
    Model,
)


class AbstractRepository(ABC):

    """Репозиторий - коллекция объектов.

    Предоставляет набор методов для выборки определенных срезов данных.
    """

    model: Model

    def get_by_id(self, id_):
        return self._base_query().get(id=id_)

    def get_by_ids(self, ids):
        return self._base_query().filter(id__in=ids)

    def add(self, obj):
        return self._save(obj)

    def update(self, obj):
        return self._save(obj)

    def _save(self, obj):
        obj.full_clean()
        return obj.save()

    def _base_query(self):
        return self.model.objects.all()
