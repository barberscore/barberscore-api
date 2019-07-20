# Django
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    path('', lambda r: HttpResponseRedirect('admin/')),
    path('admin/', admin.site.urls),
    path('bhs/', include('apps.bhs.urls')),
    path('smanager/', include('apps.smanager.urls')),
    path('rmanager/', include('apps.rmanager.urls')),
    path('jwt/', include('rest_framework_jwt.urls')),
    path('log/', include('django_fsm_log.urls')),
    path('rq/', include('django_rq.urls')),
    path('robots.txt', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),
]

if settings.DEBUG and settings.DJANGO_SETTINGS_MODULE == 'settings.dev':
    import debug_toolbar
    urlpatterns += [
        re_path(
            r'^media/(?P<path>.*)$',
            serve, {
                'document_root': settings.MEDIA_ROOT,
            }
        ),
        path('__debug__/', include(debug_toolbar.urls)),
    ]
