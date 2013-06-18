from django.conf.urls import patterns, include, url

from django.contrib.gis import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('hoods.views',
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/date/(?P<date>\d{8})/$', 'detail'),
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/date/(?P<date>\d{8})/police/$', 'police_detail'),
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/date/(?P<date>\d{8})/fire/$', 'fire_detail'),
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/date/(?P<date>\d{8})/permits/$', 'permit_detail'),
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/date/(?P<date>\d{8})/violations/$', 'violation_detail'),
    
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/date/(?P<date>today)/$', 'detail'),
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/date/(?P<date>today)/police/$', 'police_detail'),
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/date/(?P<date>today)/fire/$', 'fire_detail'),
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/date/(?P<date>today)/permits/$', 'permit_detail'),
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/date/(?P<date>today)/violations/$', 'violation_detail'),
    
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/date/(?P<date>yesterday)/$', 'detail'),
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/date/(?P<date>yesterday)/police/$', 'police_detail'),
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/date/(?P<date>yesterday)/fire/$', 'fire_detail'),
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/date/(?P<date>yesterday)/permits/$', 'permit_detail'),
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/date/(?P<date>yesterday)/violations/$', 'violation_detail'),
    
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/$', 'detail', {'date':'yesterday'}),
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/police/$', 'police_detail', {'date':'yesterday'}),
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/fire/$', 'fire_detail', {'date':'yesterday'}),
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/permits/$', 'permit_detail', {'date':'yesterday'}),
    url(r'^neighborhood/(?P<neighborhood>[\w\-]+)/violations/$', 'violation_detail', {'date':'yesterday'}),
    
    url(r'^police/$', 'police_detail', {'neighborhood':'Seattle', 'date':'yesterday'}),
    url(r'^fire/$', 'fire_detail', {'neighborhood':'Seattle', 'date':'yesterday'}),
    url(r'^permits/$', 'permit_detail', {'neighborhood':'Seattle', 'date':'yesterday'}),
    url(r'^violations/$', 'violation_detail', {'neighborhood':'Seattle', 'date':'yesterday'}),
    
    url(r'^(?P<neighborhood>[\w\-]+)/$', 'detail', {'date':'yesterday'}),
    url(r'^(?P<neighborhood>[\w\-]+)/police/$', 'police_detail', {'date':'yesterday'}),
    url(r'^(?P<neighborhood>[\w\-]+)/fire/$', 'fire_detail', {'date':'yesterday'}),
    url(r'^(?P<neighborhood>[\w\-]+)/permits/$', 'permit_detail', {'date':'yesterday'}),
    url(r'^(?P<neighborhood>[\w\-]+)/violations/$', 'violation_detail', {'date':'yesterday'}),
    
    url(r'^$', 'detail', {'neighborhood':'Seattle', 'date':'yesterday'}),
)
