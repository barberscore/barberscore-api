
# Third-Party
from rest_framework import routers

# Local
from .viewsets import PersonViewSet

router = routers.DefaultRouter(
    trailing_slash=False,
)

router.register(r'person', PersonViewSet)
urlpatterns = router.urls
