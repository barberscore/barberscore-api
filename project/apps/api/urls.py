from rest_framework import routers

from .views import (
    ConventionViewSet,
    ContestViewSet,
    AwardViewSet,
    CompetitorViewSet,
    SessionViewSet,
    GroupViewSet,
    ContestantViewSet,
    TuneViewSet,
    PersonViewSet,
    SearchViewSet,
    SongViewSet,
    SingerViewSet,
    DirectorViewSet,
    CatalogViewSet,
    ScoreViewSet,
    JudgeViewSet,
    PerformanceViewSet,
    OrganizationViewSet,
)

router = routers.DefaultRouter()

router.register(r'convention', ConventionViewSet)
router.register(r'contest', ContestViewSet)
router.register(r'award', AwardViewSet)
router.register(r'competitor', CompetitorViewSet)
router.register(r'session', SessionViewSet)
router.register(r'group', GroupViewSet)
router.register(r'contestant', ContestantViewSet)
router.register(r'person', PersonViewSet)
router.register(r'tune', TuneViewSet)
router.register(r'song', SongViewSet)
router.register(r'singer', SingerViewSet)
router.register(r'director', DirectorViewSet)
router.register(r'catalog', CatalogViewSet)
router.register(r'score', ScoreViewSet)
router.register(r'judge', JudgeViewSet)
router.register(r'performance', PerformanceViewSet)
router.register(r'organization', OrganizationViewSet)
router.register(r'search', SearchViewSet, base_name='search')
urlpatterns = router.urls
