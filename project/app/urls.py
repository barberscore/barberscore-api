# Third-Party
from rest_framework import routers

# Local
from .views import (
    AssignmentViewSet,
    AwardViewSet,
    CatalogViewSet,
    ContestantScoreViewSet,
    ContestantViewSet,
    ContestScoreViewSet,
    ContestViewSet,
    ConventionViewSet,
    EntityViewSet,
    HostViewSet,
    MembershipViewSet,
    OfficerViewSet,
    OfficeViewCSV,
    OfficeViewSet,
    PerformanceScoreViewSet,
    PerformanceViewSet,
    PerformerScoreViewSet,
    PerformerViewSet,
    PersonViewSet,
    RoundViewSet,
    ScoreViewSet,
    SessionViewSet,
    SlotViewSet,
    SongScoreViewSet,
    SongViewSet,
    SubmissionViewSet,
    UserViewSet,
    VenueViewSet,
)

router = routers.DefaultRouter(
    trailing_slash=False,
)

router.register(r'award', AwardViewSet)
router.register(r'catalog', CatalogViewSet)
router.register(r'contest', ContestViewSet)
router.register(r'contestscore', ContestScoreViewSet)
router.register(r'contestant', ContestantViewSet)
router.register(r'contestantscore', ContestantScoreViewSet)
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
router.register(r'officecsv', OfficeViewCSV)
urlpatterns = router.urls
