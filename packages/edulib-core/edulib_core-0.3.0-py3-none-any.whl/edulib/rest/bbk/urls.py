from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.bbk import (
    views,
)


router = SimpleRouter()

router.register('bbk', views.BbkViewSet, basename='bbk')
