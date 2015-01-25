from rest_framework import routers

from .views import (
    SingerViewSet,
    ChorusViewSet,
)

router = routers.SimpleRouter()
router.register(r'singers', SingerViewSet)
router.register(r'chorus', ChorusViewSet)


urlpatterns = router.urls
