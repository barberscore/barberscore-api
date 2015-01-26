from rest_framework import routers

from .views import (
    SingerViewSet,
    ChorusViewSet,
    QuartetViewSet,
)

router = routers.SimpleRouter()
router.register(r'singers', SingerViewSet)
router.register(r'choruses', ChorusViewSet)
router.register(r'quartets', QuartetViewSet)


urlpatterns = router.urls
