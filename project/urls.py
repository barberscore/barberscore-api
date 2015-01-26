from django.conf.urls import include, url
from django.contrib import admin
from ajax_select import urls as ajax_select_urls

urlpatterns = [
    url(r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('apps.api.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
