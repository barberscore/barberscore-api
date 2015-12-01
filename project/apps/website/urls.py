from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [

    # url(r'^$', views.home, name='home'),
    # url(
    #     r'^login/$',
    #     views.login,
    #     name='login',
    # ),
    # url(
    #     r'^logout/$',
    #     views.logout,
    #     name='logout',
    # ),

    # url(r'^dashboard/$', views.dashboard, name='dashboard'),
    # url(r'^contest/(?P<slug>[a-zA-Z0-9-]+)/$', views.contest, name='contest'),
    # url(r'^contest/(?P<slug>[a-zA-Z0-9-]+)/build/$', views.contest_build, name='contest_build'),
    # url(r'^contest/(?P<slug>[a-zA-Z0-9-]+)/impanel/$', views.contest_impanel, name='contest_impanel'),
    # url(r'^contest/(?P<slug>[a-zA-Z0-9-]+)/fill/$', views.contest_fill, name='contest_fill'),
    # # url(r'^contest/(?P<slug>[a-zA-Z0-9-]+)/start/$', views.contest_start, name='contest_start'),
    # url(r'^session/(?P<slug>[a-zA-Z0-9-]+)/draw/$', views.session_draw, name='session_draw'),
    # url(r'^session/(?P<slug>[a-zA-Z0-9-]+)/start/$', views.session_start, name='session_start'),
    # url(r'^performance/(?P<slug>[a-zA-Z0-9-]+)/score/$', views.performance_score, name='performance_score'),
    # url(r'^session/(?P<slug>[a-zA-Z0-9-]+)/end/$', views.session_end, name='session_end'),
    # url(r'^contest/(?P<slug>[a-zA-Z0-9-]+)/end/$', views.contest_end, name='contest_end'),

    # # Scoresheets
    # url(r'^session/(?P<slug>[a-zA-Z0-9-]+)/oss/$', views.session_oss, name='session-oss'),
    # url(r'^contest/(?P<slug>[a-zA-Z0-9-]+)/oss/$', views.contest_oss, name='contest-oss'),
    # url(r"^contest/(?P<slug>[a-zA-Z0-9-]+)/pdf/$", views.HelloPDFView.as_view())

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
