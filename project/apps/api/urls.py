from rest_framework import routers

from .views import (
    ConventionViewSet,
    ContestViewSet,
    GroupViewSet,
    ContestantViewSet,
    PerformanceViewSet,
    SingerViewSet,
    DirectorViewSet,
    NoteViewSet,
    UserViewSet,
    DistrictViewSet,
)

router = routers.DefaultRouter()

router.register(r'conventions', ConventionViewSet)
router.register(r'contests', ContestViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'contestants', ContestantViewSet)
router.register(r'performances', PerformanceViewSet)
router.register(r'singers', SingerViewSet)
router.register(r'directors', DirectorViewSet)
router.register(r'notes', NoteViewSet, 'note')
router.register(r'accounts', UserViewSet)
router.register(r'districts', DistrictViewSet)

urlpatterns = router.urls
