from django.conf.urls import url
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^search/$', views.search, name='search'),

    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt')),
    url(r'^sitemap.xml$', TemplateView.as_view(template_name='sitemap.xml')),


    url(r'^contests/$', views.ContestList.as_view(), name='contest-list'),
    url(r'^contests/(?P<slug>[a-zA-Z0-9-]+)/$', views.ContestDetail.as_view(), name='contest-detail'),

    url(r'^conventions/$', views.ConventionList.as_view(), name='convention-list'),
    url(r'^conventions/(?P<slug>[a-zA-Z0-9-]+)/$', views.ConventionDetail.as_view(), name='convention-detail'),

    url(r'^districts/$', views.DistrictList.as_view(), name='district-list'),
    url(r'^districts/(?P<slug>[a-zA-Z0-9-]+)/$', views.DistrictDetail.as_view(), name='district-detail'),

    url(r'^singers/$', views.SingerList.as_view(), name='singer-list'),
    url(r'^singers/(?P<slug>[a-zA-Z0-9-]+)/$', views.SingerDetail.as_view(), name='singer-detail'),

    url(r'^choruses/$', views.ChorusList.as_view(), name='chorus-list'),
    url(r'^choruses/(?P<slug>[a-zA-Z0-9-]+)/$', views.chorus_detail, name='chorus-detail'),

    url(r'^quartets/$', views.QuartetList.as_view(), name='quartet-list'),
    url(r'^quartets/(?P<slug>[a-zA-Z0-9-]+)/$', views.quartet_detail, name='quartet-detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
