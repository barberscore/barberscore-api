from rest_framework import routers

from .views import (
    ConventionViewSet,
    SessionViewSet,
    AwardViewSet,
    ContestantViewSet,
    RoundViewSet,
    GroupViewSet,
    PerformerViewSet,
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

router.register(r'award', AwardViewSet)
router.register(r'catalog', CatalogViewSet)
router.register(r'contestant', ContestantViewSet)
router.register(r'session', SessionViewSet)
router.register(r'performer', PerformerViewSet)
router.register(r'convention', ConventionViewSet)
router.register(r'director', DirectorViewSet)
router.register(r'group', GroupViewSet)
router.register(r'judge', JudgeViewSet)
router.register(r'singer', SingerViewSet)
router.register(r'organization', OrganizationViewSet)
router.register(r'performance', PerformanceViewSet)
router.register(r'person', PersonViewSet)
router.register(r'score', ScoreViewSet)
router.register(r'round', RoundViewSet)
router.register(r'song', SongViewSet)
router.register(r'tune', TuneViewSet)
router.register(r'search', SearchViewSet, base_name='search')
urlpatterns = router.urls
