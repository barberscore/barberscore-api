
# Third-Party
from rest_framework import routers

# Local
from .views import GroupViewSet
from .views import MemberViewSet
from .views import OfficerViewSet
from .views import PersonViewSet
from .views import ChartViewSet
from .views import RepertoryViewSet

router = routers.DefaultRouter(
    trailing_slash=False,
)

router.register(r'group', GroupViewSet)
router.register(r'member', MemberViewSet)
router.register(r'officer', OfficerViewSet)
router.register(r'person', PersonViewSet)
router.register(r'chart', ChartViewSet)
router.register(r'repertory', RepertoryViewSet)
urlpatterns = router.urls
