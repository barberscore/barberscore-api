# Django
from django.conf.urls import (
    include,
    url,
)
from django.contrib import admin
from django.http import HttpResponse

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('apps.api.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),
]
