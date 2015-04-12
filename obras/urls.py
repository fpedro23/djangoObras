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
                       url(r'^reportes/balance-general', views.balance_general),
                       url(r'^reportes/informacion-general', views.hipervinculo_informacion_general),
                       url(r'^reportes/informacion-sector', views.hipervinculo_sector),
                       url(r'^reportes/informacion-entidad', views.hipervinculo_entidad),
                       url(r'^reportes/concluidas-proceso-proyectadas',views.hipervinculo_concluidas_proceso_proyectadas),
                       url(r'^buscar-obras/', views.consulta_web),

                       # reportes predefinidos
                       url(r'^reportes-predefinidos', views.reportes_predefinidos),
                       url(r'^balance-general-ppt', views.balance_general_ppt),
                       url(r'^hiper-info-general-ppt', views.hiper_info_general_ppt),
                       url(r'^hiper-inauguradas-ppt', views.hiper_inauguradas_ppt),
                       url(r'^hiper-por-sector-ppt', views.hiper_por_sector_ppt),
                       url(r'^hiper-por-entidad-ppt', views.hiper_por_entidad_ppt),

)