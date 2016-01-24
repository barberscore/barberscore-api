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
    # url(r'^contest/(?P<slug>[a-zA-Z0-9-]+)/$', views.contest, name='contest'),
    # url(r'^contest/(?P<slug>[a-zA-Z0-9-]+)/build/$', views.contest_build, name='contest_build'),
    # url(r'^contest/(?P<slug>[a-zA-Z0-9-]+)/imsession/$', views.contest_imsession, name='contest_imsession'),
    # url(r'^contest/(?P<slug>[a-zA-Z0-9-]+)/fill/$', views.contest_fill, name='contest_fill'),
    # # url(r'^contest/(?P<slug>[a-zA-Z0-9-]+)/start/$', views.contest_start, name='contest_start'),
    # url(r'^round/(?P<slug>[a-zA-Z0-9-]+)/draw/$', views.round_draw, name='round_draw'),
    # url(r'^round/(?P<slug>[a-zA-Z0-9-]+)/start/$', views.round_start, name='round_start'),
    # url(r'^performance/(?P<slug>[a-zA-Z0-9-]+)/score/$', views.performance_score, name='performance_score'),
    # url(r'^round/(?P<slug>[a-zA-Z0-9-]+)/end/$', views.round_end, name='round_end'),
    # url(r'^contest/(?P<slug>[a-zA-Z0-9-]+)/end/$', views.contest_end, name='contest_end'),

    # Scoresheets
    # url(r'^round/(?P<slug>[a-zA-Z0-9-]+)/oss/$', views.round_oss, name='round-oss'),
    url(r'^contest/(?P<slug>[a-zA-Z0-9-]+)/oss/$', views.contest_oss, name='contest-oss'),
    url(r'^session/(?P<slug>[a-zA-Z0-9-]+)/sa/$', views.session_sa, name='session-sa'),
    url(r'^performer/(?P<slug>[a-zA-Z0-9-]+)/csa/$', views.performer_csa, name='performer-csa'),
    url(r"^contest/(?P<slug>[a-zA-Z0-9-]+)/pdf/$", views.HelloPDFView.as_view())

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
