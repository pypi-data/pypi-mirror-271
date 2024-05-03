from typing import (
    TYPE_CHECKING,
    Mapping,
)

from explicit.domain.validation.exceptions import (
    init_messages_dict,
)


if TYPE_CHECKING:
    from explicit.domain import (
        DTOBase,
    )

    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def may_skip(func):
    """Пропускает шаг валидации, если установлен флаг."""

    def wrapper(self, *args, **kwargs):
        if self._skip_chain:  # pylint: disable=protected-access
            return self

        return func(self, *args, **kwargs)

    return wrapper


class Validator:
    """Базовый класс валидатора.

    Представляет собой цепочку валидации данных, оканчивающуюся вызовом метода get_errors.
    """

    def __init__(self, data: 'DTOBase', uow: 'UnitOfWork') -> None:
        self._data = data
        self._uow = uow

        self._errors = init_messages_dict()
        self._skip_chain = False

    def get_errors(self) -> Mapping[str, list[str]]:
        """Возвращает ошибки валидации."""
        return self._errors
