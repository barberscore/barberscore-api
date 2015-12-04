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
    url(r'^award/(?P<slug>[a-zA-Z0-9-]+)/$', views.award, name='award'),
    url(r'^award/(?P<slug>[a-zA-Z0-9-]+)/build/$', views.award_build, name='award_build'),
    url(r'^award/(?P<slug>[a-zA-Z0-9-]+)/imcontest/$', views.award_imcontest, name='award_imcontest'),
    url(r'^award/(?P<slug>[a-zA-Z0-9-]+)/fill/$', views.award_fill, name='award_fill'),
    # url(r'^award/(?P<slug>[a-zA-Z0-9-]+)/start/$', views.award_start, name='award_start'),
    url(r'^session/(?P<slug>[a-zA-Z0-9-]+)/draw/$', views.session_draw, name='session_draw'),
    url(r'^session/(?P<slug>[a-zA-Z0-9-]+)/start/$', views.session_start, name='session_start'),
    url(r'^performance/(?P<slug>[a-zA-Z0-9-]+)/score/$', views.performance_score, name='performance_score'),
    url(r'^session/(?P<slug>[a-zA-Z0-9-]+)/end/$', views.session_end, name='session_end'),
    url(r'^award/(?P<slug>[a-zA-Z0-9-]+)/end/$', views.award_end, name='award_end'),

    # Scoresheets
    url(r'^session/(?P<slug>[a-zA-Z0-9-]+)/oss/$', views.session_oss, name='session-oss'),
    url(r'^award/(?P<slug>[a-zA-Z0-9-]+)/oss/$', views.award_oss, name='award-oss'),
    url(r"^award/(?P<slug>[a-zA-Z0-9-]+)/pdf/$", views.HelloPDFView.as_view())

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
