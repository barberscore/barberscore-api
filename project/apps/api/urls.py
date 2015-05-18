from rest_framework import routers

from .views import (
    ConventionViewSet,
    ContestViewSet,
    GroupViewSet,
    ContestantViewSet,
    PerformanceViewSet,
    ScheduleViewSet,
    ScoreViewSet,
    # SearchViewSet,
)

router = routers.DefaultRouter()

router.register(r'conventions', ConventionViewSet)
router.register(r'contests', ContestViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'contestants', ContestantViewSet)
# router.register(r'schedules', ScheduleViewSet)
router.register(r'performances', PerformanceViewSet)
# router.register(r'scores', ScoreViewSet)
# router.register(r'search', SearchViewSet, base_name='search')

urlpatterns = router.urls
