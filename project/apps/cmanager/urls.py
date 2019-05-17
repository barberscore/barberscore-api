
# Third-Party
from rest_framework import routers

# Local
from .views import AssignmentViewSet
from .views import AwardViewSet
from .views import ConventionViewSet

router = routers.DefaultRouter(
    trailing_slash=False,
)

router.register(r'assignment', AssignmentViewSet)
router.register(r'award', AwardViewSet, basename='award')
router.register(r'convention', ConventionViewSet)
urlpatterns = router.urls
