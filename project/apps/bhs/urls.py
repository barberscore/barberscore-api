
# Third-Party
from rest_framework import routers
from django.urls import path

# Local
from .views import AwardViewSet
from .views import GroupViewSet
from .views import PersonViewSet
from .views import ChartViewSet
from .views import ConventionViewSet
from .views import ConventionCompleteView
from .views import ConventionSyncView

router = routers.DefaultRouter(
    trailing_slash=False,
)

router.register(r'group', GroupViewSet)
router.register(r'award', AwardViewSet)
router.register(r'person', PersonViewSet)
router.register(r'chart', ChartViewSet)
router.register(r'convention', ConventionViewSet)
urlpatterns = router.urls + [
    path('convention/<uuid:pk>/complete', ConventionCompleteView.as_view(), name='convention-complete'),
    path('convention/<uuid:pk>/sync', ConventionSyncView.as_view(), name='convention-sync'),
]
