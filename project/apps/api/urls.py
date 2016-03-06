from rest_framework import routers

from .views import (
    AwardViewSet,
    CertificationViewSet,
    ChapterViewSet,
    ChartViewSet,
    ContestViewSet,
    ContestantViewSet,
    ConventionViewSet,
    GroupViewSet,
    JudgeViewSet,
    MemberViewSet,
    OrganizationViewSet,
    PerformanceViewSet,
    PerformerViewSet,
    PersonViewSet,
    RoleViewSet,
    RoundViewSet,
    ScoreViewSet,
    SessionViewSet,
    SetlistViewSet,
    SongViewSet,
    VenueViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'award', AwardViewSet)
router.register(r'certification', CertificationViewSet)
router.register(r'chapter', ChapterViewSet)
router.register(r'chart', ChartViewSet)
router.register(r'contest', ContestViewSet)
router.register(r'contestant', ContestantViewSet)
router.register(r'convention', ConventionViewSet)
router.register(r'group', GroupViewSet)
router.register(r'judge', JudgeViewSet)
router.register(r'member', MemberViewSet)
router.register(r'organization', OrganizationViewSet)
router.register(r'performance', PerformanceViewSet)
router.register(r'performer', PerformerViewSet)
router.register(r'person', PersonViewSet)
router.register(r'role', RoleViewSet)
router.register(r'round', RoundViewSet)
router.register(r'score', ScoreViewSet)
router.register(r'session', SessionViewSet)
router.register(r'setlist', SetlistViewSet)
router.register(r'song', SongViewSet)
router.register(r'venue', VenueViewSet)
urlpatterns = router.urls
