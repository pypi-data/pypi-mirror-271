from enum import (
    Enum,
)


class NamedIntEnum(int, Enum):
    """Базовый класс для набора пар число + строка."""

    def __new__(cls, value: int, label: str) -> 'NamedIntEnum':
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.label = label

        return obj

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def choices(cls) -> list[tuple[int, str]]:
        return [(member.value, member.label) for member in cls]
