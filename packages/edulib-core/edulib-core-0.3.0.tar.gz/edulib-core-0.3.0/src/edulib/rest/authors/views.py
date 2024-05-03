from rest_framework import (
    filters,
)

from edulib.core.lib_authors.domain.commands import (
    CreateAuthor,
    DeleteAuthor,
    UpdateAuthor,
)
from edulib.core.lib_authors.models import (
    LibraryAuthors,
)
from edulib.rest.authors import (
    serializers,
)
from edulib.rest.base.viewsets import (
    CommandBasedModelViewSet,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class AuthorViewSet(CommandBasedModelViewSet):
    """Эндпоинты для работы с авторами."""

    queryset = LibraryAuthors.objects.all()
    serializer_class = serializers.AuthorSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name',)
    # TODO permissions pylint: disable=fixme

    create_command = CreateAuthor
    update_command = UpdateAuthor
    delete_command = DeleteAuthor
