from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.publishings import (
    views,
)


router = SimpleRouter()

router.register('publishings', views.PublishingViewSet, basename='publishings')
