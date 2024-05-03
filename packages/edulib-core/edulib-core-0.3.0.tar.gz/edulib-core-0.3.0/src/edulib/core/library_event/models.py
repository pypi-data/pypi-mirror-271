# pylint: disable=invalid-str-returned
from django.db import (
    models,
)

from edulib.core.base.files import (
    upload_file_handler,
)
from edulib.core.base.models import (
    BaseModel,
)
from edulib.core.lib_passport.models import (
    LibPassport,
)
from edulib.core.library_event import (
    domain,
)


class LibraryEvent(BaseModel):
    """План работы библиотеки."""

    library = models.ForeignKey(
        LibPassport,
        verbose_name=domain.Event.library_id.title,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name=domain.Event.name.title,
        max_length=domain.Event.name.max_length,
    )
    place = models.CharField(
        verbose_name=domain.Event.place.title,
        max_length=domain.Event.place.max_length,
    )
    date_begin = models.DateField(
        verbose_name=domain.Event.date_begin.title,
    )
    date_end = models.DateField(
        verbose_name=domain.Event.date_end.title,
        null=True,
        blank=True,
    )
    participants = models.CharField(
        verbose_name=domain.Event.participants.title,
        max_length=domain.Event.participants.max_length,
    )
    file = models.FileField(
        verbose_name=domain.Event.file.title,
        upload_to=upload_file_handler,
        max_length=255,
        blank=True,
    )
    description = models.TextField(
        verbose_name=domain.Event.description.title,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
