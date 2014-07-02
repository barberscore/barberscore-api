from django.conf.urls import patterns, url

urlpatterns = patterns(
    'noncense.views',

    url(r'^logout/$', 'logout', name='logout'),
    url(r'^login/$', 'login', name='login'),
    url(r'^entercode/$', 'entercode', name='entercode'),
    url(r'^inbound/$', 'inbound', name='inbound'),
    url(r'^support/$', 'support', name='support'),

)
