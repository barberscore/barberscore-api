
# Third-Party
from rest_framework import routers

# Local
from .views import AppearanceViewSet
from .views import ContenderViewSet
from .views import OutcomeViewSet
from .views import PanelistViewSet
from .views import RoundViewSet
from .views import ScoreViewSet
from .views import SongViewSet

router = routers.DefaultRouter(
    trailing_slash=False,
)

router.register(r'appearance', AppearanceViewSet)
router.register(r'contender', ContenderViewSet)
router.register(r'outcome', OutcomeViewSet)
router.register(r'panelist', PanelistViewSet)
router.register(r'round', RoundViewSet)
router.register(r'score', ScoreViewSet)
router.register(r'song', SongViewSet)
urlpatterns = router.urls
