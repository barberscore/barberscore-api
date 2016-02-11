from rest_framework import routers

from .views import (
    ArrangerViewSet,
    AwardViewSet,
    ChapterViewSet,
    ConventionViewSet,
    SessionViewSet,
    ContestViewSet,
    ContestantViewSet,
    RoundViewSet,
    GroupViewSet,
    PerformerViewSet,
    TuneViewSet,
    PersonViewSet,
    SongViewSet,
    SingerViewSet,
    DirectorViewSet,
    CatalogViewSet,
    ScoreViewSet,
    JudgeViewSet,
    PerformanceViewSet,
    OrganizationViewSet,
    GroupSearchViewSet,
    PersonSearchViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'arranger', ArrangerViewSet)
router.register(r'award', AwardViewSet)
router.register(r'catalog', CatalogViewSet)
router.register(r'chapter', ChapterViewSet)
router.register(r'contest', ContestViewSet)
router.register(r'contestant', ContestantViewSet)
router.register(r'convention', ConventionViewSet)
router.register(r'director', DirectorViewSet)
router.register(r'group/search', GroupSearchViewSet, base_name='group-search')
router.register(r'group', GroupViewSet)
router.register(r'judge', JudgeViewSet)
router.register(r'organization', OrganizationViewSet)
router.register(r'performance', PerformanceViewSet)
router.register(r'performer', PerformerViewSet)
router.register(r'person/search', PersonSearchViewSet, base_name='person-search')
router.register(r'person', PersonViewSet)
router.register(r'round', RoundViewSet)
router.register(r'score', ScoreViewSet)
router.register(r'session', SessionViewSet)
router.register(r'singer', SingerViewSet)
router.register(r'song', SongViewSet)
router.register(r'tune', TuneViewSet)
urlpatterns = router.urls
