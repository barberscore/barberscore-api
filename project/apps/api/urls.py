from rest_framework import routers

from .views import (
    ConventionViewSet,
    ContestViewSet,
    GroupViewSet,
    ContestantViewSet,
    PerformanceViewSet,
    NoteViewSet,
    UserViewSet,
)

router = routers.DefaultRouter()

router.register(r'conventions', ConventionViewSet)
router.register(r'contests', ContestViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'contestants', ContestantViewSet)
router.register(r'performances', PerformanceViewSet)
router.register(r'notes', NoteViewSet, 'note')
router.register(r'accounts', UserViewSet)

urlpatterns = router.urls
