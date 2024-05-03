from rest_framework import (
    filters,
)

from edulib.core.directory.domain import (
    CreateBbk,
    DeleteBbk,
    UpdateBbk,
)
from edulib.core.directory.models import (
    Catalog,
)
from edulib.rest.base.viewsets import (
    CommandBasedModelViewSet,
)
from edulib.rest.bbk.serializers import (
    BbkSerializer,
)


class BbkViewSet(CommandBasedModelViewSet):
    """Эндпоинты для работы с разделами ББК."""

    serializer_class = BbkSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('code', 'name',)
    ordering_fields = ('code',)
    ordering = ('code',)
    # TODO permissions pylint: disable=fixme

    create_command = CreateBbk
    update_command = UpdateBbk
    delete_command = DeleteBbk

    def get_queryset(self):
        queryset = Catalog.objects.all()

        parent_id = self.request.query_params.get('parent_id')
        if parent_id:
            queryset = queryset.filter(parent=parent_id)
        else:
            queryset = queryset.filter(parent__isnull=True)

        return queryset
