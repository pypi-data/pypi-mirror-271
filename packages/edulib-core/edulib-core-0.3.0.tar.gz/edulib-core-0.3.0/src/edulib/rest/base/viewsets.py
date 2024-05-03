from rest_framework import (
    mixins,
)
from rest_framework.viewsets import (
    GenericViewSet,
)

from edulib.rest.base.mixins import (
    CommandBasedCreateModelMixin,
    CommandBasedDestroyModelMixin,
    CommandBasedUpdateModelMixin,
)


class CommandBasedModelViewSet(
    CommandBasedCreateModelMixin,
    mixins.RetrieveModelMixin,
    CommandBasedUpdateModelMixin,
    CommandBasedDestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """ModelViewSet основанный на командах."""
