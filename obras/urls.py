from django.conf.urls import patterns, url

from obras import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = patterns('',
                       # Mappings for the new (protected) implementation of the mobile API
                       url(r'^api/estados', views.EstadosEndpoint.as_view()),
                       url(r'^api/dependencias', views.DependenciasEndpoint.as_view()),
                       url(r'^api/impactos', views.ImpactosEndpoint.as_view()),
                       url(r'^api/inauguradores', views.InauguradorEndpoint.as_view()),
                       url(r'^api/clasificaciones', views.ClasificacionEndpoint.as_view()),
                       url(r'^api/inversiones', views.InversionEndpoint.as_view()),
                       url(r'^api/tiposDeObra', views.TipoDeObraEndpoint.as_view()),
                       url(r'^api/busqueda', views.BuscadorEndpoint.as_view()),
                       url(r'^api/hora', views.HoraEndpoint.as_view()),
                       url(r'^api/obras_iniciadas', views.ObrasIniciadasEndpoint.as_view()),
                       url(r'^api/obras_vencidas', views.ObrasVencidasEndpoint.as_view()),

                       url(r'^reportes/balance-general', views.balance_general),
                       url(r'^reportes/informacion-general', views.hipervinculo_informacion_general),
                       url(r'^reportes/informacion-sector', views.hipervinculo_sector),
                       url(r'^reportes/informacion-entidad', views.hipervinculo_entidad),
                       url(r'^reportes/concluidas-proceso-proyectadas',
                           views.hipervinculo_concluidas_proceso_proyectadas),

                       url(r'^buscar-obras/', views.consulta_web),
                       url(r'^consultar-obras', views.buscar_obras_web),
                       url(r'^prueba', views.ajax_prueba),

)