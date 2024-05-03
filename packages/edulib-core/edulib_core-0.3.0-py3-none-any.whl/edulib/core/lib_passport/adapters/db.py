from django.core.exceptions import (
    ObjectDoesNotExist,
)

from edulib.core.adapters.db import (
    AbstractRepository,
)
from edulib.core.lib_passport.domain.model import (
    PassportNotFound,
)
from edulib.core.lib_passport.models import (
    LibPassport,
)


class PassportRepository(AbstractRepository):

    model = LibPassport

    def get_by_id(self, id_):
        try:
            return super().get_by_id(id_)
        except ObjectDoesNotExist as exc:
            raise PassportNotFound() from exc

    def get_by_school_id(self, school_id):
        return self._base_query().filter(school_id=school_id)


passports = PassportRepository()
