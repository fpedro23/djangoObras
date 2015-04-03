from django.conf.urls import patterns, url

from obras import views


urlpatterns = patterns('',
                       # Mappings for the new (protected) implementation of the mobile API
                       url(r'^api/buscarObras', views.index),
                       url(r'^api/estados', views.EstadosEndpoint.as_view()),
                       url(r'^api/dependencias', views.DependenciasEndpoint.as_view()),
                       url(r'^api/impactos', views.ImpactosEndpoint.as_view()),
                       url(r'^api/inauguradores', views.InauguradorEndpoint.as_view()),
                       url(r'^api/clasificaciones', views.ClasificacionEndpoint.as_view()),
                       url(r'^api/inversiones', views.InversionEndpoint.as_view()),
                       url(r'^api/tiposDeObra', views.TipoDeObraEndpoint.as_view()),
)
