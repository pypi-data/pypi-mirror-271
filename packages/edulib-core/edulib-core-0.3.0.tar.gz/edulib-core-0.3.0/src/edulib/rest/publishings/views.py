from rest_framework import (
    filters,
)

from edulib.core.lib_publishings.domain.commands import (
    CreatePublishing,
    DeletePublishing,
    UpdatePublishing,
)
from edulib.core.lib_publishings.models import (
    LibraryPublishings,
)
from edulib.rest.base.viewsets import (
    CommandBasedModelViewSet,
)
from edulib.rest.publishings.serializers import (
    PublishingSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class PublishingViewSet(CommandBasedModelViewSet):
    """Эндпоинты для работы с издательствами."""

    queryset = LibraryPublishings.objects.all()
    serializer_class = PublishingSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name',)
    # TODO permissions pylint: disable=fixme

    create_command = CreatePublishing
    update_command = UpdatePublishing
    delete_command = DeletePublishing
