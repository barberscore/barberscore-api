from rest_framework import routers

from .views import (
    ConventionViewSet,
    ContestViewSet,
    GroupViewSet,
    ContestantViewSet,
    DistrictViewSet,
    SongViewSet,
    PersonViewSet,
    SearchViewSet,
    PerformanceViewSet,
    SingerViewSet,
    DirectorViewSet,
    ChartViewSet,
)

router = routers.DefaultRouter()

router.register(r'conventions', ConventionViewSet)
router.register(r'contests', ContestViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'contestants', ContestantViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'persons', PersonViewSet)
router.register(r'songs', SongViewSet)
router.register(r'performances', PerformanceViewSet)
router.register(r'singers', SingerViewSet)
router.register(r'directors', DirectorViewSet)
router.register(r'charts', ChartViewSet)
router.register(r'searches', SearchViewSet, base_name='search')
urlpatterns = router.urls
