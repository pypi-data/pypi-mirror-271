from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.events.views import (
    EventViewSet,
)


router = SimpleRouter()

router.register('events', EventViewSet, basename='events')
