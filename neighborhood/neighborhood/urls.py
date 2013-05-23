from django.conf.urls import patterns, include, url

from django.contrib.gis import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'neighborhood.views.home', name='home'),
    # url(r'^neighborhood/', include('neighborhood.foo.urls')),
    
    url(r'^neighborhood/(?P<neighborhood>\w+)/date/(?P<date>\d+)/', 'hoods.views.detail'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
