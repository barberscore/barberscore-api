from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('apps.api.urls')),
    # url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^website/', include('apps.website.urls', namespace='website')),
    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
