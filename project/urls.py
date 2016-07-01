# Third-Party
from rest_framework_jwt import views

# Django
from django.conf import settings
from django.conf.urls import (
    include,
    url,
)
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-token-auth/', views.obtain_jwt_token, name='obtain-jwt-token'),
    url(r'^api-token-refresh/', views.refresh_jwt_token),
    url(r'^api-token-verify/', views.verify_jwt_token),
    url(r'^api/', include('apps.api.urls')),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
