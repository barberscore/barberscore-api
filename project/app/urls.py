# Third-Party
from rest_framework import routers

# Local
from .views import (
    AssignmentViewSet,
    AwardViewSet,
    CatalogViewSet,
    ContestantViewSet,
    ContestViewSet,
    ContestScoreViewSet,
    ConventionViewSet,
    EntityViewSet,
    HostViewSet,
    MembershipViewSet,
    OfficeViewSet,
    OfficerViewSet,
    PerformanceViewSet,
    PerformanceScoreViewSet,
    PerformerViewSet,
    PerformerScoreViewSet,
    PersonViewSet,
    RoundViewSet,
    ScoreViewSet,
    SessionViewSet,
    SlotViewSet,
    SongViewSet,
    SongScoreViewSet,
    SubmissionViewSet,
    VenueViewSet,
    UserViewSet,
)

router = routers.DefaultRouter(
    trailing_slash=False,
)

router.register(r'award', AwardViewSet)
router.register(r'catalog', CatalogViewSet)
router.register(r'contest', ContestViewSet)
router.register(r'contestscore', ContestScoreViewSet)
router.register(r'contestant', ContestantViewSet)
router.register(r'contestantscore', ContestantViewSet)
router.register(r'convention', ConventionViewSet)
router.register(r'entity', EntityViewSet)
router.register(r'host', HostViewSet)
router.register(r'assignment', AssignmentViewSet)
router.register(r'membership', MembershipViewSet)
router.register(r'office', OfficeViewSet)
router.register(r'officer', OfficerViewSet)
router.register(r'performance', PerformanceViewSet)
router.register(r'performancescore', PerformanceScoreViewSet)
router.register(r'performer', PerformerViewSet)
router.register(r'performerscore', PerformerScoreViewSet)
router.register(r'person', PersonViewSet)
router.register(r'round', RoundViewSet)
router.register(r'score', ScoreViewSet)
router.register(r'session', SessionViewSet)
router.register(r'submission', SubmissionViewSet)
router.register(r'slot', SlotViewSet)
router.register(r'song', SongViewSet)
router.register(r'songscore', SongScoreViewSet)
router.register(r'venue', VenueViewSet)
router.register(r'user', UserViewSet)
urlpatterns = router.urls
