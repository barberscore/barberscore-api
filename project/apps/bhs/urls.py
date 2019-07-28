
# Third-Party
from rest_framework import routers

# Local
from .views import AwardViewSet
from .views import GroupViewSet
from .views import PersonViewSet
from .views import ChartViewSet
from .views import ConventionViewSet

router = routers.DefaultRouter(
    trailing_slash=False,
)

router.register(r'group', GroupViewSet)
router.register(r'award', AwardViewSet, basename='award')
router.register(r'person', PersonViewSet)
router.register(r'chart', ChartViewSet)
router.register(r'convention', ConventionViewSet)
urlpatterns = router.urls
