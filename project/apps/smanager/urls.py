
# Third-Party
from rest_framework import routers

# Local
from .views import AssignmentViewSet
from .views import ConventionViewSet
from .views import ContestViewSet
from .views import EntryViewSet
from .views import SessionViewSet

router = routers.DefaultRouter(
    trailing_slash=False,
)


router.register(r'assignment', AssignmentViewSet)
router.register(r'convention', ConventionViewSet)
router.register(r'contest', ContestViewSet)
router.register(r'entry', EntryViewSet)
router.register(r'session', SessionViewSet)
urlpatterns = router.urls
