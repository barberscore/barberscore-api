from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.rate.views',

    url(r'rating/$', 'ratings', name='ratings'),
    url(r'rating/(?P<performance>[\w-]+)/$', 'rating', name='rating'),
    url(r'prediction/enter/$', 'prediction', name='prediction'),
    url(r'prediction/$', 'predictions', name='predictions'),
)
