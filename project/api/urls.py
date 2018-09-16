
# Third-Party
from rest_framework import routers

# Local
from .views import AppearanceViewSet
from .views import AssignmentViewSet
from .views import AwardViewSet
from .views import ChartViewSet
from .views import CompetitorViewSet
from .views import ContestantViewSet
from .views import ContestViewSet
from .views import ConventionViewSet
from .views import EntryViewSet
from .views import GrantorViewSet
from .views import GridViewSet
from .views import GroupViewSet
from .views import MemberViewSet
from .views import OfficerViewSet
from .views import OfficeViewSet
from .views import PanelistViewSet
from .views import PersonViewSet
from .views import RepertoryViewSet
from .views import RoundViewSet
from .views import ScoreViewSet
from .views import SessionViewSet
from .views import SongViewSet
from .views import StateLogViewSet
from .views import UserViewSet
from .views import VenueViewSet

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
router.register(r'competitor', CompetitorViewSet)
router.register(r'entry', EntryViewSet)
router.register(r'grantor', GrantorViewSet)
router.register(r'grid', GridViewSet)
router.register(r'group', GroupViewSet)
router.register(r'member', MemberViewSet)
router.register(r'office', OfficeViewSet)
router.register(r'officer', OfficerViewSet)
router.register(r'panelist', PanelistViewSet)
router.register(r'person', PersonViewSet)
router.register(r'repertory', RepertoryViewSet)
router.register(r'round', RoundViewSet)
router.register(r'score', ScoreViewSet)
router.register(r'session', SessionViewSet)
router.register(r'song', SongViewSet)
router.register(r'user', UserViewSet)
router.register(r'venue', VenueViewSet)
router.register(r'statelog', StateLogViewSet)
urlpatterns = router.urls
