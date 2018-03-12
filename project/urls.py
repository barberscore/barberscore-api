# Django
# Third-Party
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from django.views.static import serve


from django.conf import settings
from django.urls import (
    include,
    path,
    re_path,
)
from django.contrib import admin
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)

schema_view = get_schema_view(
    title='Barberscore API',
)

urlpatterns = [
    path('', lambda r: HttpResponseRedirect('admin/')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('rq/', include('django_rq.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('schema/', schema_view),
    path('docs/', include_docs_urls(title='Documentation', description='API Documentation')),
    path('robots.txt', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),
]

if settings.DEBUG:
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
