from rest_framework.serializers import (
    ModelSerializer,
)

from edulib.core.lib_registry.models import (
    LibMarkInformProduct,
)


class InfoProductMarkSerializer(ModelSerializer):

    class Meta:
        model = LibMarkInformProduct
        fields = ('id', 'code', 'name')
