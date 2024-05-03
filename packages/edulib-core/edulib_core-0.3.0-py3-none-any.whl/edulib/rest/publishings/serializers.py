from rest_framework.serializers import (
    ModelSerializer,
)

from edulib.core.lib_publishings.models import (
    LibraryPublishings,
)


class PublishingSerializer(ModelSerializer):

    class Meta:
        model = LibraryPublishings
        fields = ('id', 'name')
