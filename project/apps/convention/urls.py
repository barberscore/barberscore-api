from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.convention.views',

    url(r'contestant/$', 'contestants', name='contestants'),
    url(r'contestant/(?P<slug>[\w-]+)/$', 'contestant', name='contestant'),

    url(r'performance/$', 'performances', name='performances'),
    url(r'performance/(?P<slug>[\w-]+)/$', 'performance', name='performance'),
)
