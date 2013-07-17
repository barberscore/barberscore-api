from django.conf.urls import patterns, include, url
from django.conf import settings

from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(

    '',
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^about/', TemplateView.as_view(template_name='about.html')),
    url(r'^logout/', 'django.contrib.auth.views.logout', name='logout'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^search/', include('haystack.urls')),

    url(r'^', include('apps.bbs.urls')),
    url(r'^', include('apps.profile.urls')),
    # url(r'^', include('apps.rate.urls')),
    url(r'^', include('noncense.urls')),


)


if settings.DEBUG:
    urlpatterns += patterns(
        (r'media/(?P<path>.*)', 'django.views.staticserve', {'document_root': settings.MEDIA_ROOT})
    )
