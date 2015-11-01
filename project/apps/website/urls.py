from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(
        r'^login/$',
        views.login,
        name='login',
    ),
    url(
        r'^logout/$',
        views.logout,
        name='logout',
    ),

    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^contest/(?P<contest_slug>[a-zA-Z0-9-]+)/$', views.contest, name='contest'),
    url(r'^session/(?P<session_slug>[a-zA-Z0-9-]+)/$', views.session, name='session'),
    url(r'^performance/(?P<performance_slug>[a-zA-Z0-9-]+)/$', views.performance, name='performance'),

    url(r'^session/(?P<session_slug>[a-zA-Z0-9-]+)/oss/$', views.session_oss, name='session-oss'),
    url(r'^contest/(?P<contest_slug>[a-zA-Z0-9-]+)/oss/$', views.contest_oss, name='contest-oss'),
    url(r"^contest/(?P<slug>[a-zA-Z0-9-]+)/pdf/$", views.HelloPDFView.as_view())
    # url(r'^merge/$', views.merge, name='merge'),
    # url(r'^merge/person/$', views.persons, name='persons'),
    # url(r'^merge/person/all/$', views.all_persons, name='all-persons'),
    # url(r'^merge/chorus/$', views.choruses, name='choruses'),
    # url(r'^merge/chorus/all/$', views.all_choruses, name='all-choruses'),
    # url(r'^merge/quartet/$', views.quartets, name='quartets'),
    # url(r'^merge/quartet/all/$', views.all_quartets, name='all-quartets'),
    # url(r'^merge/song/$', views.songs, name='songs'),
    # url(r'^merge/song/all/$', views.all_songs, name='all-songs'),
    # url(r'^merge/manual-persons/$', views.manual_persons, name='manual-persons'),
    # url(r'^merge/manual-groups/$', views.manual_groups, name='manual-groups'),
    # url(r'^merge/manual-songs/$', views.manual_songs, name='manual-songs'),

    # url(r'^merge/merge-groups/(?P<parent_id>[a-zA-Z0-9-]+)/(?P<child_id>[a-zA-Z0-9-]+)/$', views.merge_groups, name='merge-groups'),
    # url(r'^merge/remove-group/(?P<parent_id>[a-zA-Z0-9-]+)/$', views.remove_group, name='remove-group'),
    # url(r'^merge/merge-songs/(?P<parent_id>[a-zA-Z0-9-]+)/(?P<child_id>[a-zA-Z0-9-]+)/$', views.merge_songs, name='merge-songs'),
    # url(r'^merge/remove-song/(?P<parent_id>[a-zA-Z0-9-]+)/$', views.remove_song, name='remove-song'),
    # url(r'^merge/merge-persons/(?P<parent_id>[a-zA-Z0-9-]+)/(?P<child_id>[a-zA-Z0-9-]+)/$', views.merge_persons, name='merge-persons'),
    # url(r'^merge/remove-person/(?P<parent_id>[a-zA-Z0-9-]+)/$', views.remove_person, name='remove-person'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
