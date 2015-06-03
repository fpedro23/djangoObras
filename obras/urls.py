from django.conf.urls import patterns, url

from obras import views
from obras import api


urlpatterns = patterns('',
                       # Inician mappings del API
                       # Mappings Catalogos
                       url(r'^api/estados', api.EstadosEndpoint.as_view()),
                       url(r'^api/dependencias', api.DependenciasEndpoint.as_view()),
                       url(r'^api/impactos', api.ImpactosEndpoint.as_view()),
                       url(r'^api/inauguradores', api.InauguradorEndpoint.as_view()),
                       url(r'^api/clasificaciones', api.ClasificacionEndpoint.as_view()),
                       url(r'^api/inversiones', api.InversionEndpoint.as_view()),
                       url(r'^api/tiposDeObra', api.TipoDeObraEndpoint.as_view()),

                        url(r'^api/subdependencias_arbol', api.DependenciasTreeEndpoint.as_view()),
                       url(r'^api/subdependencias_flat', api.SubependenciasFlatEndpoint.as_view()),

                       # Mappings Busqueda
                       url(r'^api/busqueda', api.BuscadorEndpoint.as_view()),

                       # Mappings Reportes
                       url(r'^api/obras_iniciadas', api.ObrasIniciadasEndpoint.as_view()),
                       url(r'^api/obras_vencidas', api.ObrasVencidasEndpoint.as_view()),
                       url(r'^api/obras_dependencia', api.ObrasForDependenciaEndpoint.as_view()),
                       url(r'^api/inicio', api.ReporteInicioEndpoint.as_view()),

                       # Otors endpoints
                       url(r'^api/hora', api.HoraEndpoint.as_view()),
                       # Fin mappings del API

                       url(r'^reportes/balance-general', views.balance_general),
                       url(r'^reportes/informacion-general', views.hipervinculo_informacion_general),
                       url(r'^reportes/informacion-sector', views.hipervinculo_sector),
                       url(r'^reportes/informacion-entidad', views.hipervinculo_entidad),
                       url(r'^reportes/concluidas-proceso-proyectadas',views.hipervinculo_concluidas_proceso_proyectadas),
                       url(r'^reportes/concluidas-proceso-proyectadas',
                           views.hipervinculo_concluidas_proceso_proyectadas),

                       url(r'^buscar-obras/', views.consulta_web),
                       url(r'^consultar-obras', views.buscar_obras_web),
                       url(r'^prueba', views.ajax_prueba),

                       # reportes predefinidos
                       #url(r'^reportes-predefinidos', views.reportes_predefinidos),
                       # url(r'^balance-general-ppt', views.balance_general_ppt),
                       # url(r'^hiper-info-general-ppt', views.hiper_info_general_ppt),
                       # url(r'^hiper-inauguradas-ppt', views.hiper_inauguradas_ppt),
                       # url(r'^hiper-por-sector-ppt', views.hiper_por_sector_ppt),
                       # url(r'^hiper-por-entidad-ppt', views.hiper_por_entidad_ppt),
)