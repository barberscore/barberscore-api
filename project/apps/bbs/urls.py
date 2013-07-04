from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.bbs.views',
    url(r'^$', 'home', name='home'),
    # url(r'score/(?P<performance>\d+)$', 'score', name='score'),
    url(r'success/$', 'success', name='success'),
    url(r'profile/$', 'profile', name='profile'),


    url(r'performance/$', 'performances', name='performances'),
    url(r'contestant/$', 'contestants', name='contestants'),


    url(r'contestant/(?P<contestant>[\w-]+)/$', 'contestant', name='contestant'),
    url(r'performance/(?P<performance>[\w-]+)/$', 'performance', name='performance'),
    url(r'contest/(?P<contest>[\w-]+)/$', 'contest', name='schedule'),
    url(r'score/(?P<contest>[\w-]+)/$', 'score', name='score'),


    url(r'contest/$', 'contests', name='contests'),


)
