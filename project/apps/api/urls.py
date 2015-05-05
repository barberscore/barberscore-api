from rest_framework import routers

from .views import (
    SingerViewSet,
    ChorusViewSet,
    QuartetViewSet,
    ConventionViewSet,
    ContestViewSet,
    PerformanceViewSet,
    ContestantViewSet,
)

router = routers.SimpleRouter()
router.register(r'singers', SingerViewSet)
router.register(r'choruses', ChorusViewSet)
router.register(r'contests', ContestViewSet)
router.register(r'performances', PerformanceViewSet)
router.register(r'quartets', QuartetViewSet)
router.register(r'conventions', ConventionViewSet)
router.register(r'contestants', ContestantViewSet)


urlpatterns = router.urls
