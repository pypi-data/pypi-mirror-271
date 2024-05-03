from django.urls import (
    include,
    path,
)
from rest_framework.routers import (
    DefaultRouter,
)

from edulib.rest.utils.tools import (
    import_submodules,
)


router = DefaultRouter()

for module in import_submodules('edulib.rest', '.urls'):
    router.registry.extend(module.router.registry)


urlpatterns = [
    path('', include(router.urls)),
]
