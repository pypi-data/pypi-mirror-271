from rest_framework.serializers import (
    ModelSerializer,
)

from edulib.core.lib_authors.models import (
    LibraryAuthors,
)


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = LibraryAuthors
        fields = ('id', 'name')
