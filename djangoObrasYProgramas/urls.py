from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^obras/', include('obras.urls')),
)
