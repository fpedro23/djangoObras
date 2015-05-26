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

    # user auth URLs
    
        # user auth URLs

    #url(r'^login$', 'obras.views.login', name='login'),
    #url(r'^auth_view$', 'obras.views.auth_view', name='auth_view'),
    #url(r'^logout$', 'obras.views.logout', name='logout'),
    #url(r'^loggedin$', 'obras.views.loggedin', name='loggedin'),
    #url(r'^invalid_login$', 'obras.views.invalid_login', name='invalid_login'),
    #url(r'^create_user$', 'obras.views.create_user', name='create_user'),
    #url(r'^register_success$', 'obras.views.register_success', name='register_success'),
    #url(r'^create_obra$', 'obras.views.create_obra', name='create_obra'),
    #url(r'^create_authuser$', 'obras.views.create_authuser', name='create_authuser'),
    #url(r'^see_map$', 'obras.views.see_map', name='see_map'),
    #url(r'^do_chart$', 'obras.views.do_chart', name='do_chart'),
    #url(r'^coords_save$', 'coords_save', name='coords_save'),
    
    
    
    url(r'^obras/catalogo$', 'obras.views.catalogo', name='catalogo'),
    url(r'^obras/c_clasificacion$', 'obras.views.c_clasificacion', name='c_clasificacion'),
    url(r'^obras/c_dependencia$', 'obras.views.c_dependencia', name='c_dependencia'),
     url(r'^obras/c_subdependencia$', 'obras.views.c_subdependencia', name='c_subdependencia'),
    url(r'^obras/c_inaugurador$', 'obras.views.c_inaugurador', name='c_inaugurador'),
    url(r'^obras/c_impacto$', 'obras.views.c_impacto', name='c_impacto'),
    url(r'^obras/c_inversion$', 'obras.views.c_inversion', name='c_inversion'),
    url(r'^obras/movimientos$', 'obras.views.movimientos', name='movimientos'),
    url(r'^obras/consultas$', 'obras.views.consultas', name='consultas'),
    url(r'^obras/c_filtro$', 'obras.views.c_filtro', name='c_filtro'),
    url(r'^obras/c_guardada$', 'obras.views.c_guardada', name='c_guardada'),
    url(r'^obras/c_predefinida$', 'obras.views.c_predefinida', name='c_predefinida'),
    url(r'^obras/usuarios$', 'obras.views.usuarios', name='usuarios'),
    url(r'^obras/consulta_filtros', 'obras.views.consulta_web', name='consulta_filtros'),

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
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
