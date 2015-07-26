from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^person/$', views.persons, name='persons'),
    url(r'^chorus/$', views.choruses, name='choruses'),
    url(r'^quartet/$', views.quartets, name='quartets'),
    url(r'^song/$', views.songs, name='songs'),
    url(r'^merge-groups/(?P<parent>[a-zA-Z0-9-]+)/(?P<child>[a-zA-Z0-9-]+)/$', views.merge_groups, name='merge_groups'),
    url(r'^remove-group/(?P<parent>[a-zA-Z0-9-]+)/$', views.remove_group, name='remove_group'),
    url(r'^merge-songs/(?P<parent>[a-zA-Z0-9-]+)/(?P<child>[a-zA-Z0-9-]+)/$', views.merge_songs, name='merge_songs'),
    url(r'^remove-song/(?P<parent>[a-zA-Z0-9-]+)/$', views.remove_song, name='remove_song'),
    url(r'^merge-persons/(?P<parent>[a-zA-Z0-9-]+)/(?P<child>[a-zA-Z0-9-]+)/$', views.merge_persons, name='merge_persons'),
    url(r'^remove-person/(?P<parent>[a-zA-Z0-9-]+)/$', views.remove_person, name='remove_person'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
