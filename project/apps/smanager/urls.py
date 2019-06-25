
# Third-Party
from rest_framework import routers

# Local
from .views import ContestViewSet
from .views import ContestantViewSet
from .views import EntryViewSet
from .views import SessionViewSet

router = routers.DefaultRouter(
    trailing_slash=False,
)

router.register(r'contest', ContestViewSet)
router.register(r'contestant', ContestantViewSet)
router.register(r'entry', EntryViewSet)
router.register(r'session', SessionViewSet)
urlpatterns = router.urls
