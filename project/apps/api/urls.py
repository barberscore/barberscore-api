from rest_framework import routers

from .views import (
    ConventionViewSet,
    ChorusViewSet,
    QuartetViewSet,
    SearchViewSet,
)

router = routers.SimpleRouter()

router.register(r'conventions', ConventionViewSet)
router.register(r'choruses', ChorusViewSet)
router.register(r'quartets', QuartetViewSet)
router.register(r'search', SearchViewSet, base_name='search')

urlpatterns = router.urls
