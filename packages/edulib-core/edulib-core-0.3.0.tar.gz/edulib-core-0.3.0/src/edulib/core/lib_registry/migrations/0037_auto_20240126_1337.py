from django.contrib.postgres.aggregates.general import (
    ArrayAgg,
)
from django.db import (
    migrations,
)
from django.db.migrations.operations.special import (
    RunPython,
)
from django.db.models.expressions import (
    OuterRef,
    Subquery,
)


def forwards(apps, *_):
    model = apps.get_model(
        'lib_registry.LibRegistryEntry'
    )

    model.objects.update(
        study_level_ids=Subquery(
            model.objects.filter(id=OuterRef('id')).annotate(
                levels=ArrayAgg('study_levels')
            ).values('levels')
        )
    )


def get_operations():
    from django.apps import (
        apps,
    )

    target_model = 'core.StudyLevel'

    try:
        apps.get_model(target_model)

    except LookupError:
        pass

    else:
        yield RunPython(forwards)


class Migration(migrations.Migration):

    dependencies = [
        ('lib_registry', '0036_libregistryentry_study_level_ids'),
    ]

    operations = list(get_operations())
