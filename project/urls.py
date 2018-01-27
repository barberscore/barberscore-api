# Django
# Third-Party
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

from django.conf import settings
from django.conf.urls import (
    include,
    url,
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
    url(r'^$', lambda r: HttpResponseRedirect('admin/')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    # url(r'^bhs/', include('bhs.urls')),
    url(r'^rq/', include('django_rq.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^schema/', schema_view),
    url(r'^docs/', include_docs_urls(title='Documentation', description='API Documentation')),
    url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
