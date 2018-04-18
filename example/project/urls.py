# from toolbox import views
from django.conf import settings
from django.contrib import admin
from django.views.static import serve
from django.conf.urls import include, url
admin.autodiscover()


urlpatterns = (
    # url(r'^$', views.index, name="index"),
    # url(r'^elections/$', views.election_list, name="election_list"),
    # url(r'^elections/(?P<id>(.*))/$', views.election_detail, name="election_detail"),
    # url(r'^candidatecontest/(?P<pk>(.*))/$', views.CandidateContestDetail.as_view(), name="candidatecontest_detail"),
    # url(r'^posts/(?P<pk>(.*))/$', views.PostDetail.as_view(), name="post_detail"),
    # url(r'^people/$', views.PersonList.as_view(), name="person_list"),
    # url(r'^people/(?P<pk>(.*))/$', views.PersonDetail.as_view(), name="person_detail"),
    # url(r'^candidates-no-party/$', views.CandidateNoPartyList.as_view(), name="candidatenoparty_list"),
    # url(r'^primaries-no-party/$', views.PrimaryNoPartyList.as_view(), name="primarynoparty_list"),
    # url(r'^parties/$', views.PartyList.as_view(), name="party_list"),
    # url(r'^parties/(?P<pk>(.*))/$', views.PartyDetail.as_view(), name="party_detail"),
    # url(r'^committees/$', views.CommitteeList.as_view(), name="committee_list"),
    # url(r'^committees/(?P<pk>(.*))/$', views.CommitteeDetail.as_view(), name="committee_detail"),
    # url(r'^filings/(?P<pk>(.*))/$', views.FilingDetail.as_view(), name="filing_detail"),
    # url(r'^filing-actions/(?P<pk>(.*))/$', views.FilingActionDetail.as_view(), name="filingaction_detail"),
    url(r'^admin/', admin.site.urls),
    # url(r'^static/(?P<path>.*)$', serve, {
    #     'document_root': settings.STATIC_ROOT,
    #     'show_indexes': True,
    # }),
)
