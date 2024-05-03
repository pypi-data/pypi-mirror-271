from datetime import (
    date,
)
from typing import (
    List,
    Optional,
)

from explicit.messagebus.commands import (
    Command,
)


class DeliverExamples(Command):

    """Команда "Сдать экземпляры"."""

    ids: List[int]
    fact_delivery_date: Optional[date]
    special_notes: Optional[str]
