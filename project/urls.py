#


# Third-Party
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

# Django
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.static import serve

schema_view = get_schema_view(
    title='Barberscore API',
)

urlpatterns = [
    path('', lambda r: HttpResponseRedirect('admin/')),
    path('admin/', admin.site.urls),
    path('bhs/', include('apps.bhs.urls')),
    path('cmanager/', include('apps.cmanager.urls')),
    path('smanager/', include('apps.smanager.urls')),
    path('rmanager/', include('apps.rmanager.urls')),
    path('api/', include('rest_framework_jwt.urls')),
    path('log/', include('django_fsm_log.urls')),
    path('rq/', include('django_rq.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('schema/', schema_view),
    path('docs/', include_docs_urls(title='Barberscore Documentation')),
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
