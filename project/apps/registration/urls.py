
# Third-Party
from rest_framework import routers

# Local
from .views import AssignmentViewSet
from .views import ContestViewSet
from .views import EntryViewSet
from .views import SessionViewSet
from .views import RepertoryViewSet

router = routers.DefaultRouter(
    trailing_slash=False,
)


router.register(r'assignment', AssignmentViewSet)
router.register(r'contest', ContestViewSet)
router.register(r'entry', EntryViewSet)
router.register(r'session', SessionViewSet)
router.register(r'repertory', RepertoryViewSet)
urlpatterns = router.urls
