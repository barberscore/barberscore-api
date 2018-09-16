
# Third-Party
from rest_framework import routers

# Local
from .views import HumanViewSet
from .views import StructureViewSet

router = routers.DefaultRouter(
    trailing_slash=False,
)

router.register(r'human', HumanViewSet)
router.register(r'structure', StructureViewSet)
urlpatterns = router.urls
