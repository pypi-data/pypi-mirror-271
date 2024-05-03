from rest_framework import (
    serializers,
)
from rest_framework.serializers import (
    ModelSerializer,
)

from edulib.core.library_event.models import (
    LibraryEvent,
)


class EventSerializer(ModelSerializer):

    library_id = serializers.IntegerField(
        label='Библиотека',
        min_value=1,
    )

    class Meta:
        model = LibraryEvent
        fields = (
            'id',
            'library_id',
            'name',
            'place',
            'date_begin',
            'date_end',
            'participants',
            'file',
            'description',
        )
