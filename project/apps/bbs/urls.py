from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.bbs.views',

    url(r'^$', 'home', name='home'),

    url(r'contest/$', 'contests', name='contests'),
    url(r'contest/(?P<slug>[\w-]+)/$', 'contest', name='contest'),

    url(r'contestant/$', 'contestants', name='contestants'),
    url(r'contestant/(?P<slug>[\w-]+)/$', 'contestant', name='contestant'),

    url(r'score/$', 'scores', name='scores'),
    url(r'score/(?P<slug>[\w-]+)/$', 'score', name='score'),

    url(r'quartet/$', 'quartets', name='quartets'),
    url(r'chorus/$', 'choruses', name='choruses'),


)
