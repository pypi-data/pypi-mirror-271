from rest_framework import (
    filters,
)
from rest_framework.viewsets import (
    ReadOnlyModelViewSet,
)

from edulib.core.lib_registry.models import (
    LibMarkInformProduct,
)
from edulib.rest.info_product_marks.serializers import (
    InfoProductMarkSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class InfoProductMarkViewSet(ReadOnlyModelViewSet):
    """Эндпоинты для работы  со знаками информационной продукции."""

    queryset = LibMarkInformProduct.objects.all()
    serializer_class = InfoProductMarkSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name',)
