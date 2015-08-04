from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^person/$', views.persons, name='persons'),
    url(r'^person/all/$', views.all_persons, name='all-persons'),
    url(r'^chorus/$', views.choruses, name='choruses'),
    url(r'^chorus/all/$', views.all_choruses, name='all-choruses'),
    url(r'^quartet/$', views.quartets, name='quartets'),
    url(r'^quartet/all/$', views.all_quartets, name='all-quartets'),
    url(r'^song/$', views.songs, name='songs'),
    url(r'^song/all/$', views.all_songs, name='all-songs'),
    # url(r'^build-chorus/$', views.build_chorus, name='build-chorus'),
    # url(r'^build-quartet/$', views.build_quartet, name='build-quartet'),
    # url(r'^build-song/$', views.build_song, name='build-song'),
    # url(r'^build-person/$', views.build_person, name='build-person'),
    url(r'^merge-groups/(?P<parent_id>[a-zA-Z0-9-]+)/(?P<child_id>[a-zA-Z0-9-]+)/$', views.merge_groups, name='merge-groups'),
    url(r'^remove-group/(?P<parent_id>[a-zA-Z0-9-]+)/$', views.remove_group, name='remove-group'),
    url(r'^merge-songs/(?P<parent_id>[a-zA-Z0-9-]+)/(?P<child_id>[a-zA-Z0-9-]+)/$', views.merge_songs, name='merge-songs'),
    url(r'^remove-song/(?P<parent_id>[a-zA-Z0-9-]+)/$', views.remove_song, name='remove-song'),
    url(r'^merge-persons/(?P<parent_id>[a-zA-Z0-9-]+)/(?P<child_id>[a-zA-Z0-9-]+)/$', views.merge_persons, name='merge-persons'),
    url(r'^remove-person/(?P<parent_id>[a-zA-Z0-9-]+)/$', views.remove_person, name='remove-person'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
