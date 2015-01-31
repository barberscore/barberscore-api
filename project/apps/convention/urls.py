from django.conf.urls import patterns, url

urlpatterns = patterns(
    'convention.views',

    url(r'^contestant/(?P<slug>[\w-]+)/$', 'contestant', name='contestant'),
    url(r'^performance/$', 'performances', name='performances'),
    url(r'^contest/$', 'contests', name='contests'),
    url(r'^search/$', 'search', name='search'),

)
