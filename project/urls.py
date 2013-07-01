from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('apps.bbs.urls')),
    # url(r'^', include('noncense.urls')),

)

# Uncomment these two lines and comment the stock url conf below
# if you wish to use the "Noncense" auth backend.

urlpatterns += patterns(
    '',
    url(r'noncense_request/$', 'noncense.views.noncense_request', {'template_name': 'noncense/request.html'}, name='noncense_request'),
    url(r'noncense_response/$', 'noncense.views.noncense_response', {'template_name': 'noncense/response.html'}, name='noncense_response'),
    url(r'logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
)

# urlpatterns += patterns(
#     '',
#     # url(r'login/$', 'django.contrib.auth.views.login', name='login'),
#     url(r'logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
# )
