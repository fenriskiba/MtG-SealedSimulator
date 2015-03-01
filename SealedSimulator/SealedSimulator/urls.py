from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^cardlist/', include('cardlist.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
