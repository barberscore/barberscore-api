from django.conf.urls import patterns, url

urlpatterns = patterns(
    'profile.views',
    url(r'profile/$', 'profile', name='profile'),
)
