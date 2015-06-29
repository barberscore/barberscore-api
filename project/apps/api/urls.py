from rest_framework import routers

from .views import (
    ConventionViewSet,
    ContestViewSet,
    GroupViewSet,
    ContestantViewSet,
    SingerViewSet,
    DirectorViewSet,
    NoteViewSet,
    UserViewSet,
    DistrictViewSet,
    SongViewSet,
    SearchViewSet,
)

router = routers.DefaultRouter()

router.register(r'conventions', ConventionViewSet)
router.register(r'contests', ContestViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'contestants', ContestantViewSet)
router.register(r'singers', SingerViewSet)
router.register(r'directors', DirectorViewSet)
router.register(r'notes', NoteViewSet, 'note')
router.register(r'accounts', UserViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'songs', SongViewSet)
router.register(r'searches', SearchViewSet, base_name='search')
urlpatterns = router.urls
