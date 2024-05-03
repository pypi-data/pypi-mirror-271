from rest_framework.serializers import (
    ModelSerializer,
)

from edulib.core.lib_example_types.models import (
    LibraryExampleType,
)


class ExampleTypeSerializer(ModelSerializer):

    class Meta:
        model = LibraryExampleType
        fields = ('id', 'name', 'release_method')
