from explicit.django.unit_of_work import (
    BaseUnitOfWork,
)


class UnitOfWork(BaseUnitOfWork):
    """Единица работы (бизнес-транзакция)."""
