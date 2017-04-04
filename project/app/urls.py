# Third-Party
from rest_framework import routers

# Local
from .views import (
    AssignmentViewSet,
    AwardViewSet,
    CatalogViewSet,
    ContestantPrivateViewSet,
    ContestantViewSet,
    ContestPrivateViewSet,
    ContestViewSet,
    ConventionViewSet,
    EntityViewSet,
    MembershipViewSet,
    OfficerViewSet,
    OfficeViewCSV,
    OfficeViewSet,
    PerformancePrivateViewSet,
    PerformanceViewSet,
    PerformerPrivateViewSet,
    PerformerViewSet,
    PersonViewSet,
    RepertoryViewSet,
    RoundViewSet,
    ScoreViewSet,
    SessionViewSet,
    SlotViewSet,
    SongPrivateViewSet,
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
router.register(r'contestprivate', ContestPrivateViewSet)
router.register(r'contestant', ContestantViewSet)
router.register(r'contestantprivate', ContestantPrivateViewSet)
router.register(r'convention', ConventionViewSet)
router.register(r'entity', EntityViewSet)
router.register(r'assignment', AssignmentViewSet)
router.register(r'membership', MembershipViewSet)
router.register(r'office', OfficeViewSet)
router.register(r'officer', OfficerViewSet)
router.register(r'performance', PerformanceViewSet)
router.register(r'performanceprivate', PerformancePrivateViewSet)
router.register(r'performer', PerformerViewSet)
router.register(r'performerprivate', PerformerPrivateViewSet)
router.register(r'person', PersonViewSet)
router.register(r'repertory', RepertoryViewSet)
router.register(r'round', RoundViewSet)
router.register(r'score', ScoreViewSet)
router.register(r'session', SessionViewSet)
router.register(r'submission', SubmissionViewSet)
router.register(r'slot', SlotViewSet)
router.register(r'song', SongViewSet)
router.register(r'songprivate', SongPrivateViewSet)
router.register(r'venue', VenueViewSet)
router.register(r'user', UserViewSet)
router.register(r'officecsv', OfficeViewCSV)
urlpatterns = router.urls
