from django.conf.urls import patterns, include, url

from django.contrib.gis import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('hoods.views',
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/date/(?P<date>\d{8})/', 'detail'),
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/date/(?P<date>today)/', 'detail'),
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/date/(?P<date>yesterday)/', 'detail'),
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/', 'detail', {'date':'yesterday'}),
    url(r'^(?P<neighborhood>[\w\-]+)/', 'detail', {'date':'yesterday'}),
    url(r'^$', 'detail', {'neighborhood':'Seattle', 'date':'yesterday'}),
)
