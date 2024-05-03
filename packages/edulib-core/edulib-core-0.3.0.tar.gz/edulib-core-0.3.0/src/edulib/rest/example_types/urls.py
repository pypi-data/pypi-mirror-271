from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.example_types import (
    views,
)


router = SimpleRouter()

router.register('example-types', views.ExampleTypeViewSet, basename='example-types')
