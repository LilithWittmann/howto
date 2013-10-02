from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'shared.views.home', name='home'),
    url(r'^js_templates.mustache$', 'shared.views.js_templates', name="js_templates"),
    # url(r'^settings/', include('settings.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^howto/', include('howto.urls')),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
)
