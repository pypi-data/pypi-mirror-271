from itertools import (
    product,
)


def modify(*objects, **params):
    """Добавляет/изменяет атрибуты объекта(ов)."""
    for obj, (key, value) in product(objects, params.items()):
        setattr(obj, key, value)
