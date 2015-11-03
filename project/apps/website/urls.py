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
    url(r'^contest/(?P<slug>[a-zA-Z0-9-]+)/$', views.contest, name='contest'),




    url(r'^session/(?P<slug>[a-zA-Z0-9-]+)/$', views.session, name='session'),
    url(r'^performance/(?P<slug>[a-zA-Z0-9-]+)/$', views.performance, name='performance'),

    url(r'^session/(?P<slug>[a-zA-Z0-9-]+)/oss/$', views.session_oss, name='session-oss'),
    url(r'^contest/(?P<slug>[a-zA-Z0-9-]+)/oss/$', views.contest_oss, name='contest-oss'),
    url(r"^contest/(?P<slug>[a-zA-Z0-9-]+)/pdf/$", views.HelloPDFView.as_view())

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
