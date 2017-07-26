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
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT,
        'show_indexes': True,
    }),
)
