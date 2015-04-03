from django.conf.urls import patterns, url

from obras import views


urlpatterns = patterns('',
                       # Mappings for the new (protected) implementation of the mobile API
                       url(r'^api/buscarObras', views.index),

                       )
