from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    # Examples:
    url(r'create/ajax', create_page, name='create_page'),
    url(r'create', create_view, name='create_page_view'),
    url(r'^edit$', edit_page, name='edit_page'),
    url(r'^tags/(?P<tag>[-\w]+)$', view_tags, name='view_tags'),
    url(r'^(?P<slug>[-\w]+)/edit$', edit_page_view, name='edit_page_view'),
    url(r'^(?P<slug>[-\w]+)$', view, name='view_page'),
    

    # url(r'^settings/', include('settings.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
