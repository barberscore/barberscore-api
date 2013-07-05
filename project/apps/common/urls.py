from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.common.views',

    url(r'profile/$', 'profile', name='profile'),
    url(r'success/$', 'success', name='success'),

)
