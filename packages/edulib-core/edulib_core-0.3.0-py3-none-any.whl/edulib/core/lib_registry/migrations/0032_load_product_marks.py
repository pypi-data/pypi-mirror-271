"""Дата миграция."""
from django.db import (
    migrations,
)


_INFORM_PRODUCT_MARKS = (
    ('0+', 'для детей всех возрастов'),
    ('6+', 'для детей старше 6 лет'),
    ('12+', 'для детей старше 12 лет'),
    ('16+', 'для детей старше 16 лет'),
    ('18+', 'запрещено для детей'),
)


def forwards(apps, schema_editor):
    """Добавляет знаки информационной продукции."""
    LibMarkInformProduct = apps.get_model(  # noqa: N806
        'lib_registry',
        'LibMarkInformProduct',
    )
    if not LibMarkInformProduct.objects.count():
        LibMarkInformProduct.objects.bulk_create([
            LibMarkInformProduct(code=code, name=name)
            for code, name in _INFORM_PRODUCT_MARKS
        ])


class Migration(migrations.Migration):
    """Миграция."""

    dependencies = [
        ('lib_registry', '0031_auto_20210730_0026'),
    ]

    operations = [
        migrations.RunPython(forwards, reverse_code=migrations.RunPython.noop),
    ]
