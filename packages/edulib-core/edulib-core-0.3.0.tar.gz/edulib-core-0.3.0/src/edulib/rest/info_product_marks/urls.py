from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.info_product_marks import (
    views,
)


router = SimpleRouter()

router.register('info_product_marks', views.InfoProductMarkViewSet, basename='info_product_marks')
