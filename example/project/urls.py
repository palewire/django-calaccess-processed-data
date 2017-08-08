from toolbox import views
from django.conf import settings
from django.contrib import admin
from django.views.static import serve
from django.conf.urls import include, url
admin.autodiscover()


urlpatterns = (
    url(r'^$', views.election_list, name="election_list"),
    url(r'^election/(?P<id>(.*))/$', views.election_detail, name="election_detail"),
    url(r'^candidatecontest/(?P<id>(.*))/$', views.candidatecontest_detail, name="candidatecontest_detail"),
    url(r'^post/(?P<pk>(.*))/$', views.PostDetail.as_view(), name="post_detail"),
    url(r'^person/(?P<pk>(.*))/$', views.PersonDetail.as_view(), name="person_detail"),
    url(r'^candidates-no-party/$', views.CandidateNoPartyList.as_view(), name="candidatenoparty_list"),
    url(r'^primaries-no-party/$', views.PrimaryNoPartyList.as_view(), name="primarynoparty_list"),
    url(r'^parties/$', views.PartyList.as_view(), name="party_list"),
    url(r'^parties/(?P<pk>(.*))/$', views.PartyDetail.as_view(), name="party_detail"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT,
        'show_indexes': True,
    }),
)
