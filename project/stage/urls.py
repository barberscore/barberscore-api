
# Third-Party
from rest_framework import routers

# Local
from .views import GridViewSet
from .views import VenueViewSet

router = routers.DefaultRouter(
    trailing_slash=False,
)
router.register(r'grid', GridViewSet)
router.register(r'venue', VenueViewSet)
urlpatterns = router.urls
