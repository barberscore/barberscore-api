
# Third-Party
from rest_framework import routers

# Local
from .views import AppearanceViewSet
from .views import ContenderViewSet
from .views import ContestantViewSet
from .views import ContestViewSet
from .views import EntryViewSet
from .views import OutcomeViewSet
from .views import PanelistViewSet
from .views import RoundViewSet
from .views import ScoreViewSet
from .views import SessionViewSet
from .views import SongViewSet
from .views import StateLogViewSet
from .views import UserViewSet

router = routers.DefaultRouter(
    trailing_slash=False,
)

router.register(r'appearance', AppearanceViewSet)
router.register(r'contest', ContestViewSet)
router.register(r'contender', ContenderViewSet)
router.register(r'contestant', ContestantViewSet)
router.register(r'entry', EntryViewSet)
router.register(r'outcome', OutcomeViewSet)
router.register(r'panelist', PanelistViewSet)
router.register(r'round', RoundViewSet)
router.register(r'score', ScoreViewSet)
router.register(r'session', SessionViewSet)
router.register(r'song', SongViewSet)
router.register(r'user', UserViewSet)
router.register(r'statelog', StateLogViewSet)
urlpatterns = router.urls
