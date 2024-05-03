from rest_framework import (
    filters,
)

from edulib.core.lib_example_types.domain.commands import (
    CreateExampleType,
    DeleteExampleType,
    UpdateExampleType,
)
from edulib.core.lib_example_types.models import (
    LibraryExampleType,
)
from edulib.rest.base.viewsets import (
    CommandBasedModelViewSet,
)
from edulib.rest.example_types.serializers import (
    ExampleTypeSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class ExampleTypeViewSet(CommandBasedModelViewSet):
    """Эндпоинты для работы с типами библиотечных экземпляров."""

    queryset = LibraryExampleType.objects.all()
    serializer_class = ExampleTypeSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name',)
    # TODO permissions pylint: disable=fixme

    create_command = CreateExampleType
    update_command = UpdateExampleType
    delete_command = DeleteExampleType
