# from toolbox import views
from django.conf import settings
from django.contrib import admin
from django.views.static import serve
from django.urls import re_path
admin.autodiscover()


urlpatterns = (
    re_path(r'^admin/', admin.site.urls),
)
