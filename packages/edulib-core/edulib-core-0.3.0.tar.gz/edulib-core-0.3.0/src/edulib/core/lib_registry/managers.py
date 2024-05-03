from django.db import (
    models,
)
from django.db.models.expressions import (
    Case,
    F,
    When,
)

from ..lib_example_types.models import (
    LibraryExampleType,
)


class LibRegistryExampleQuerySet(models.QuerySet):

    def with_inv_or_card_num_val(self):
        return self.annotate(
            inv_or_card_num_val=Case(
                When(
                    lib_reg_entry__type_id=LibraryExampleType.CLASSBOOK_ID,
                    then=F("card_number")
                ),
                default=F("inv_number"),
                output_field=models.CharField()
            )
        )


class LibRegistyExampleManager(models.Manager):

    def get_queryset(self):
        return LibRegistryExampleQuerySet(self.model, using=self._db)

    def with_inv_or_card_num_val(self):
        return self.get_queryset().with_inv_or_card_num_val()
