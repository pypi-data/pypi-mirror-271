from rest_framework.serializers import (
    ModelSerializer,
)

from edulib.core.lib_sources.models import (
    LibrarySource,
)


class SourceSerializer(ModelSerializer):
    class Meta:
        model = LibrarySource
        fields = ('id', 'name', 'school_id')


class SourceUpdateSerializer(ModelSerializer):
    class Meta:
        model = LibrarySource
        fields = ('id', 'name')
