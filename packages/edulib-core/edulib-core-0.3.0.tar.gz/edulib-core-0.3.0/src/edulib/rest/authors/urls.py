from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.authors import (
    views,
)


router = SimpleRouter()

router.register('authors', views.AuthorViewSet, basename='authors')
