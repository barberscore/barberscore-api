from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers

from apps.convention.views import (
    ContestantViewSet,
    PerformanceViewSet,
    ContestViewSet,
)

router = routers.DefaultRouter()
router.register(r'contestant', ContestantViewSet)
router.register(r'performance', PerformanceViewSet)
router.register(r'contest', ContestViewSet)

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
