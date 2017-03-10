# Django
from django.conf import settings
from django.conf.urls import (
    include,
    url,
)
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

schema_view = get_schema_view(
    title='Barberscore API',
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('app.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^schema/', schema_view),
    url(r'^docs/', include_docs_urls(title='Foobar', description='foo to the bar')),
    url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
