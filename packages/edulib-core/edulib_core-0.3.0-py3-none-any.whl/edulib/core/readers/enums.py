from edulib.core.base.domain import (
    BaseEnumerate,
)


class RequestStatusEnum(BaseEnumerate):

    """Перечисление статусов заявки."""

    REQUEST_SENT = 1
    REQUEST_PROCESSED = 2
    values = {
        REQUEST_SENT: 'Заявка отправлена',
        REQUEST_PROCESSED: 'Заявка обработана',
    }
