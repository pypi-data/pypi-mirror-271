import datetime

from django.core.exceptions import (
    ValidationError,
)


def check_schedule(label, from_val, to_val):
    # Проверка на указание полного интервала
    if bool(from_val) ^ bool(to_val):
        raise ValidationError(
            f'Время работы библиотеки "{label}" с "{from_val}" по "{to_val}" задано неверно.'
        )

    # Проверка на указание корректного интервала ( c < по)
    if from_val and to_val:
        from_val_dt = datetime.datetime.strptime(from_val, '%H:%M')
        to_val_dt = datetime.datetime.strptime(to_val, '%H:%M')
        if from_val_dt >= to_val_dt:
            raise ValidationError(
                f'Время завершения работы библиотеки "{to_val}" "{label}" '
                f'должно быть больше времени начала работы "{from_val}"'
            )
