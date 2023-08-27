
# Third-Party
from rest_framework import routers

# Local
from .views import OrganizationViewSet

router = routers.DefaultRouter(
    trailing_slash=False,
)


router.register(r'organization', OrganizationViewSet)
urlpatterns = router.urls
