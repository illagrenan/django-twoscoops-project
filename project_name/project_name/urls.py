import sys

from django.conf.urls import patterns, include, url
from django.contrib import admin

from {{ project_name }}.settings import local as settings

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^', include('web.urls', namespace='web')),

                       ############
                       # ADMIN:
                       ############

                       url(r'^grappelli/', include('grappelli.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
)


if (len(sys.argv) > 1):
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT}))