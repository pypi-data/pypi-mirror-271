from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
)

from edulib.core.directory.models import (
    Catalog,
)


class BbkSerializer(ModelSerializer):

    parent_id = IntegerField(
        label='Идентификатор родительского раздела',
        required=False,
        allow_null=True,
        min_value=1,
    )

    class Meta:
        model = Catalog
        fields = ('id', 'code', 'name', 'parent_id')
