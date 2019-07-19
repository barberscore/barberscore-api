
# Third-Party
from rest_framework import routers

# Local

router = routers.DefaultRouter(
    trailing_slash=False,
)

urlpatterns = router.urls
