from rest_framework import (
    filters,
)

from edulib.core.lib_sources.domain.commands import (
    CreateSource,
    DeleteSource,
    UpdateSource,
)
from edulib.core.lib_sources.models import (
    LibrarySource,
)
from edulib.rest.base.viewsets import (
    CommandBasedModelViewSet,
)
from edulib.rest.sources.serializers import (
    SourceSerializer,
    SourceUpdateSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class SourceViewSet(CommandBasedModelViewSet):
    """Эндпоинты для работы с источниками поступления."""

    queryset = LibrarySource.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name',)
    # TODO permissions pylint: disable=fixme

    create_command = CreateSource
    update_command = UpdateSource
    delete_command = DeleteSource

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return SourceUpdateSerializer
        return SourceSerializer
