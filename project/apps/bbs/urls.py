from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.bbs.views',
    url(r'^$', 'home', name='home'),
    # url(r'score/(?P<performance>\d+)$', 'score', name='score'),
    url(r'success/$', 'success', name='success'),
    url(r'profile/$', 'profile', name='profile'),


    url(r'performance/$', 'performances', name='performances'),
    url(r'contestant/$', 'contestants', name='contestants'),
    url(r'rating/$', 'ratings', name='ratings'),


    url(r'contestant/(?P<contestant>[\w-]+)/$', 'contestant', name='contestant'),
    url(r'performance/(?P<performance>[\w-]+)/$', 'performance', name='performance'),
    url(r'contest/(?P<contest>[\w-]+)/(?P<contest_round>[\w-]+)/$', 'contest', name='contest'),
    url(r'rating/(?P<performance>[\w-]+)/$', 'rating', name='rating'),


    url(r'contest/$', 'contests', name='contests'),
    # url(r'contest/(?P<contest>[\w-]+)/$', 'contest', name='contest'),


)
