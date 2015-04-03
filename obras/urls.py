from django.conf.urls import patterns, url

from obras import views


urlpatterns = patterns(
    '',
    url(r'^reportes/balance-general', views.balance_general),
    url(r'^reportes/informacion-general', views.hipervinculo_informacion_general),
    url(r'^reportes/informacion-sector', views.hipervinculo_sector),
    url(r'^reportes/informacion-entidad', views.hipervinculo_entidad),
    url(r'^reportes/concluidas-proceso-proyectadas', views.hipervinculo_concluidas_proceso_proyectadas),
)