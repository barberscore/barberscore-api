from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView

from rest_framework import routers

from apps.convention.viewsets import (
    ContestantViewSet,
    PerformanceViewSet,
    ContestViewSet,
)

# Routers used by REST Framework
router = routers.DefaultRouter()
router.register(r'contestant', ContestantViewSet)
router.register(r'performance', PerformanceViewSet)
router.register(r'contest', ContestViewSet)

urlpatterns = patterns(
    '',

    # Website
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^faq/$', TemplateView.as_view(template_name='faq.html'), name='faq'),
    url(r'^links/$', TemplateView.as_view(template_name='links.html'), name='links'),
    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt'), name='robots'),
    url(r'^sitemap.xml$', TemplateView.as_view(template_name='sitemap.xml'), name='sitemap'),

    # Application
    url(r'', include('apps.convention.urls')),
    url(r'', include('apps.noncense.urls')),

    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # REST Framework
    url(r'^api/v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),


) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
