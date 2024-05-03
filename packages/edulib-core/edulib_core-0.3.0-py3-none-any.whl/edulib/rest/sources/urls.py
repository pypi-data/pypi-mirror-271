from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.sources import (
    views,
)


router = SimpleRouter()


router.register('sources', views.SourceViewSet, basename='sources')
