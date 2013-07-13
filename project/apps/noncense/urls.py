from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.noncense.views',
    url(r'^login', 'login', name='login'),
    url(r'^callback', 'callback', name='callback'),
    url(r'^logout', 'logout', name='logout'),
)
