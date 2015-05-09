from rest_framework import routers

from .views import (
    ConventionViewSet,
    ChorusViewSet,
    QuartetViewSet,
)

router = routers.SimpleRouter()

router.register(r'conventions', ConventionViewSet)
router.register(r'choruses', ChorusViewSet)
router.register(r'quartets', QuartetViewSet)

urlpatterns = router.urls
