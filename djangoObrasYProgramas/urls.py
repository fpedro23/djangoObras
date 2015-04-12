from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^obras/', include('obras.urls')),
    # user auth URLs

    url(r'^login$', 'obras.views.login', name='login'),
    url(r'^auth_view$', 'obras.views.auth_view', name='auth_view'),
    url(r'^logout$', 'obras.views.logout', name='logout'),
    url(r'^loggedin$', 'obras.views.loggedin', name='loggedin'),
    url(r'^invalid_login$', 'obras.views.invalid_login', name='invalid_login'),
    url(r'^create_user$', 'obras.views.create_user', name='create_user'),
    url(r'^register_success$', 'obras.views.register_success', name='register_success'),
    url(r'^create_obra$', 'obras.views.create_obra', name='create_obra'),
    url(r'^create_authuser$', 'obras.views.create_authuser', name='create_authuser'),
    url(r'^see_map$', 'obras.views.see_map', name='see_map'),
    url(r'^do_chart$', 'obras.views.do_chart', name='do_chart'),
    url(r'^coords_save$', 'coords_save', name='coords_save'),
)
