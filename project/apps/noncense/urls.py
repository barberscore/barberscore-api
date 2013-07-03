from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.noncense.views',
    url(r'noncense_request/$', 'noncense_request', name='noncense_request'),
    url(r'noncense_response/$', 'noncense_response', name='noncense_response'),
    url(r'alternate_login/$', 'alt_login', name='alt_login'),

)

urlpatterns += patterns(
    '',
    url(r'logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
)
