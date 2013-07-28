from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'web.views.default_page', name='default_page'),
                       # url(r'^(?P<foo_slug>[-\w]+)$', 'web.views.foo_detail', name='foo_detail'),
)