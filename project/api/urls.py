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
    EntryViewSet,
    GrantorViewSet,
    GroupViewSet,
    MemberViewSet,
    OfficerViewSet,
    OfficeViewSet,
    OrganizationViewSet,
    PanelistViewSet,
    ParticipantViewSet,
    PersonViewSet,
    RepertoryViewSet,
    RoundViewSet,
    ScoreViewSet,
    SessionViewSet,
    SlotViewSet,
    SongViewSet,
    StateLogViewSet,
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
router.register(r'entry', EntryViewSet)
router.register(r'grantor', GrantorViewSet)
router.register(r'group', GroupViewSet)
router.register(r'member', MemberViewSet)
router.register(r'office', OfficeViewSet)
router.register(r'officer', OfficerViewSet)
router.register(r'organization', OrganizationViewSet)
router.register(r'panelist', PanelistViewSet)
router.register(r'participant', ParticipantViewSet)
router.register(r'person', PersonViewSet)
router.register(r'repertory', RepertoryViewSet)
router.register(r'round', RoundViewSet)
router.register(r'score', ScoreViewSet)
router.register(r'session', SessionViewSet)
router.register(r'slot', SlotViewSet)
router.register(r'song', SongViewSet)
router.register(r'user', UserViewSet)
router.register(r'venue', VenueViewSet)
router.register(r'log', StateLogViewSet)
urlpatterns = router.urls
