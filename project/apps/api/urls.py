# Third-Party
from rest_framework import routers

# Local
from .views import (
    AwardViewSet,
    CertificationViewSet,
    ChapterViewSet,
    ChartViewSet,
    ContestantViewSet,
    ContestantScoreViewSet,
    ContestViewSet,
    ConventionViewSet,
    GroupViewSet,
    JudgeViewSet,
    MemberViewSet,
    OrganizationViewSet,
    PerformanceViewSet,
    PerformanceScoreViewSet,
    PerformerViewSet,
    PerformerScoreViewSet,
    PersonViewSet,
    RoleViewSet,
    RoundViewSet,
    ScoreViewSet,
    SessionViewSet,
    SongViewSet,
    SongScoreViewSet,
    SubmissionViewSet,
    VenueViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'award', AwardViewSet)
router.register(r'certification', CertificationViewSet)
router.register(r'chapter', ChapterViewSet)
router.register(r'chart', ChartViewSet)
router.register(r'contest', ContestViewSet)
router.register(r'contestant', ContestantViewSet)
router.register(r'contestantscore', ContestantScoreViewSet)
router.register(r'convention', ConventionViewSet)
router.register(r'group', GroupViewSet)
router.register(r'judge', JudgeViewSet)
router.register(r'member', MemberViewSet)
router.register(r'organization', OrganizationViewSet)
router.register(r'performance', PerformanceViewSet)
router.register(r'performancescore', PerformanceScoreViewSet)
router.register(r'performer', PerformerViewSet)
router.register(r'performerscore', PerformerScoreViewSet)
router.register(r'person', PersonViewSet)
router.register(r'role', RoleViewSet)
router.register(r'round', RoundViewSet)
router.register(r'score', ScoreViewSet)
router.register(r'session', SessionViewSet)
router.register(r'submission', SubmissionViewSet)
router.register(r'song', SongViewSet)
router.register(r'songscore', SongScoreViewSet)
router.register(r'venue', VenueViewSet)
urlpatterns = router.urls
