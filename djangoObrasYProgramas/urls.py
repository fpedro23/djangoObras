from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^obras/', include('obras.urls')),
    url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^chaining/', include('smart_selects.urls')),

    url(r'^obras/ayuda$', 'obras.views.ayuda', name='ayuda'),
    url(r'^obras/catalogo$', 'obras.views.catalogo', name='catalogo'),
    url(r'^obras/c_clasificacion$', 'obras.views.c_clasificacion', name='c_clasificacion'),
    url(r'^obras/c_dependencia$', 'obras.views.c_dependencia', name='c_dependencia'),
    url(r'^obras/c_subdependencia$', 'obras.views.c_subdependencia', name='c_subdependencia'),
    url(r'^obras/c_inaugurador$', 'obras.views.c_inaugurador', name='c_inaugurador'),
    url(r'^obras/c_impacto$', 'obras.views.c_impacto', name='c_impacto'),
    url(r'^obras/c_inversion$', 'obras.views.c_inversion', name='c_inversion'),
    url(r'^obras/movimientos$', 'obras.views.movimientos', name='movimientos'),
    url(r'^obras/obra/modifica$', 'obras.views.modifica', name='modifica'),
    url(r'^obras/consultas$', 'obras.views.consultas', name='consultas'),
    url(r'^obras/c_filtro$', 'obras.views.c_filtro', name='c_filtro'),
    url(r'^obras/c_guardada$', 'obras.views.c_guardada', name='c_guardada'),
    url(r'^obras/c_predefinida$', 'obras.views.c_predefinida', name='c_predefinida'),
    url(r'^obras/usuarios$', 'obras.views.usuarios', name='usuarios'),
    url(r'^obras/consulta_filtros', 'obras.views.consulta_web', name='consulta_filtros'),
    url(r'^obras/consulta_predefinidos', 'obras.views.reportes_predefinidos', name='consulta_predefinidos'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
