from datetime import (
    date,
)

from django.db.models import (
    Q,
)

from edulib.core.adapters.db import (
    AbstractRepository,
)

from ..models import (
    IssuanceDelivery,
)


class IssuanceDeliveryRepository(AbstractRepository):

    model = IssuanceDelivery

    def get_issued(self):
        """Экземпляры, находящиеся "на руках"."""
        return self._base_query().filter(
            Q(
                Q(fact_delivery_date__isnull=True) |
                Q(fact_delivery_date__gt=date.today())
            )
        )

    def get_issued_for_reader(self, reader_id):
        """Экземпляры, находящиеся "на руках" у читателя."""
        return self.get_issued().filter(
            reader__id=reader_id,
            example__writeoff_date__isnull=True,
        ).order_by('ex_number')


issuance_deliveries = IssuanceDeliveryRepository()
