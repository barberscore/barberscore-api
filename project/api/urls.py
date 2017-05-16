# Third-Party
from rest_framework import routers

# Local
from .views import (
    AppearanceViewSet,
    AssignmentViewSet,
    AwardViewSet,
    ChartViewSet,
    ContestantViewSet,
    ContestViewSet,
    ConventionViewSet,
    EntityViewSet,
    EntryViewSet,
    MemberViewSet,
    OfficerViewSet,
    OfficeViewSet,
    ParticipantViewSet,
    PersonViewSet,
    RepertoryViewSet,
    RoundViewSet,
    ScoreViewSet,
    SessionViewSet,
    SlotViewSet,
    SongViewSet,
    SubmissionViewSet,
    UserViewSet,
    VenueViewSet,
)

router = routers.DefaultRouter(
    trailing_slash=False,
)

router.register(r'appearance', AppearanceViewSet)
router.register(r'assignment', AssignmentViewSet)
router.register(r'award', AwardViewSet, base_name='award')
router.register(r'chart', ChartViewSet)
router.register(r'contest', ContestViewSet)
router.register(r'contestant', ContestantViewSet)
router.register(r'convention', ConventionViewSet)
router.register(r'entity', EntityViewSet)
router.register(r'entry', EntryViewSet)
router.register(r'member', MemberViewSet)
router.register(r'office', OfficeViewSet)
router.register(r'officer', OfficerViewSet)
router.register(r'participant', ParticipantViewSet)
router.register(r'person', PersonViewSet)
router.register(r'repertory', RepertoryViewSet)
router.register(r'round', RoundViewSet)
router.register(r'score', ScoreViewSet)
router.register(r'session', SessionViewSet)
router.register(r'slot', SlotViewSet)
router.register(r'song', SongViewSet)
router.register(r'submission', SubmissionViewSet)
router.register(r'user', UserViewSet)
router.register(r'venue', VenueViewSet)
urlpatterns = router.urls
