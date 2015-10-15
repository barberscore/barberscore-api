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
    CatalogViewSet,
    ScoreViewSet,
    JudgeViewSet,
    EventViewSet,
    AwardViewSet,
)

router = routers.DefaultRouter()

router.register(r'convention', ConventionViewSet)
router.register(r'contest', ContestViewSet)
router.register(r'group', GroupViewSet)
router.register(r'contestant', ContestantViewSet)
router.register(r'district', DistrictViewSet)
router.register(r'person', PersonViewSet)
router.register(r'song', SongViewSet)
router.register(r'performance', PerformanceViewSet)
router.register(r'singer', SingerViewSet)
router.register(r'director', DirectorViewSet)
router.register(r'catalog', CatalogViewSet)
router.register(r'score', ScoreViewSet)
router.register(r'judge', JudgeViewSet)
router.register(r'event', EventViewSet)
router.register(r'award', AwardViewSet)
router.register(r'search', SearchViewSet, base_name='search')
urlpatterns = router.urls
