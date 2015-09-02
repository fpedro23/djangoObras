from django.conf.urls import patterns, url

from obras import views
from obras import api
from django.conf import settings


urlpatterns = patterns('',
                       # Inician mappings del API
                       # Mappings Catalogos
                       url(r'^api/estados', api.EstadosEndpoint.as_view()),
                       url(r'^api/dependencias', api.DependenciasEndpoint.as_view()),
                       url(r'^api/subdependencias', api.Subdependencias_forId_Endpoint.as_view()),
                       url(r'^api/impactos', api.ImpactosEndpoint.as_view()),
                       url(r'^api/inauguradores', api.InauguradorEndpoint.as_view()),
                       url(r'^api/clasificaciones', api.ClasificacionEndpoint.as_view()),
                       url(r'^api/inversiones', api.InversionEndpoint.as_view()),
                       url(r'^api/tiposDeObra', api.TipoDeObraEndpoint.as_view()),
                       url(r'^api/instanciasEjecutoras', api.InstanciaEjecutoraEndpoint.as_view()),
                       url(r'^api/numeroObrasPendientes', api.NumeroObrasPendientes.as_view()),
                       url(r'^api/noTrabajo', api.ReporteNoTrabajoEndpoint.as_view()),
                       url(r'^api/busqueda', api.BuscadorEndpoint.as_view()),
                       url(r'^api/listar', api.ListarEndpoint.as_view()),
                       url(r'^api/PptxVista', api.PptxEndpoint.as_view()),
                       url(r'^api/ReportePP', api.PptxReporteEndpoint.as_view()),
                       url(r'^api/inicio', api.ReporteInicioEndpoint.as_view()),
                       url(r'^api/subdependencias_arbol', api.DependenciasTreeEndpoint.as_view()),
                       url(r'^api/subdependencias_flat', api.SubependenciasFlatEndpoint.as_view()),
                       url(r'^api/dependencia_imagen', api.DependenciasIdEndpoint.as_view()),
                       url(r'^api/idUnico', api.IdUnicoEndpoint.as_view()),
                       url(r'^api/idIpad', api.IdUnicoEndpointIpad.as_view()),
                       url(r'^api/obras_por_autorizar', api.ReporteObrasPorAutorizar.as_view()),
                       url(r'^api/obras_iniciadas', api.ObrasIniciadasEndpoint.as_view()),
                       url(r'^api/PptxIniciadas', api.ObrasIniciadasPptxEndpoint.as_view()),
                       url(r'^api/PptxVencidas', api.ObrasVencidasPptxEndpoint.as_view()),
                       url(r'^api/PptxBitacora', api.ReporteNoTrabajoPptxEndpoint.as_view()),
                       url(r'^api/obras_vencidas', api.ObrasVencidasEndpoint.as_view()),
                       url(r'^api/obras_por_dependencia', api.ObrasForDependenciaEndpoint.as_view()),
                       url(r'^api/hora_ultima_actualizacion', api.HoraUltimaActualizacion.as_view()),
                       url(r'^api/municipios_por_estado', api.MunicipiosForEstadosEndpoint.as_view()),


                       # Mappings Busqueda
                       url(r'^api/busqueda', api.BuscadorEndpoint.as_view()),


                       url(r'^api/id_unico', api.IdUnicoEndpoint.as_view()),

                       # Mappings Reportes
                       #url(r'^obras_iniciadas', views.obras_iniciadas),
                       #url(r'^obras_vencidas', views.obras_vencidas),
                       #url(r'^obras_dependencia', views.obras_for_dependencia),
                       #url(r'^api/inicio', api.ReporteInicioEndpoint.as_view()),

                       # Otros endpoints
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
                       url(r'^videos', views.videos),
                       url(r'^ver_video', views.ver_video),
                       url(r'^manuales-Pdf', views.manualesPdf),

                       url('^ficha', views.fichaTecnica),
                       url(r'^reportes-predefinidos', views.reportes_predefinidos),
                       url(r'^balance-general-ppt', views.balance_general_ppt),
                       url(r'^hiper-info-general-ppt', views.hiper_info_general_ppt),
                       url(r'^hiper-concluidas-ppt', views.hiper_concluidas_ppt),
                       url(r'^hiper-inauguradas-ppt', views.hiper_inauguradas_ppt),
                       url(r'^hiper-por-sector-ppt', views.hiper_por_sector_ppt),
                       url(r'^hiper-por-entidad-ppt', views.hiper_por_entidad_ppt),
                       url(r'^hiper-interestatal-ppt', views.hiper_interestatal_ppt),
                       url(r'^hiper-nacional-ppt', views.hiper_nacional_ppt),
                       url(r'^hiper-rangos-ppt', views.hiper_rangos_ppt),

                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
                       url(r'^register-by-token',views.register_by_access_token),
)