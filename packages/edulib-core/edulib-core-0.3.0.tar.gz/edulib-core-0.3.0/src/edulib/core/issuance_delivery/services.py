from . import (
    domain,
)
from .adapters.db import (
    issuance_deliveries,
)


def deliver_examples(command: domain.DeliverExamples):
    """Сдача экземпляра."""

    objs = issuance_deliveries.get_by_ids(command.ids)
    for obj in objs:
        obj.fact_delivery_date = command.delivery_date
        obj.special_notes = command.special_notes
        issuance_deliveries.update(obj)
