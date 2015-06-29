# Create your views here.
import os, sys
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test

from obras.tools import *
from obras.BuscarObras import BuscaObra
from pptx.util import Pt
import json
# from pptx import Presentation
from obras.models import *
from obras.models import Obra
import datetime

from obras.BuscarObras import BuscarObras
from django.shortcuts import render_to_response
from oauth2_provider.models import AccessToken

from pptx import Presentation
from django.core.servers.basehttp import FileWrapper
import mimetypes
from django.http import StreamingHttpResponse

def get_user_for_token(token):
    if token:
        return AccessToken.objects.get(token=token).user
    else:
        return None

def register_by_access_token(request):

    #del request.session['access_token']

    if request.session.get('access_token'):
        token = {
        'access_token': request.session.get('access_token'),
        'token_type': 'Bearer'
    }
        return JsonResponse(token)
    else:
        #user = get_user_for_token('3DVteYz9OIH6gvQDyYX78GOpHKXgPy'
        user = request.user
        return get_access_token(user,request)

def ayuda(request):
    return render_to_response('admin/obras/ayuda/c_ayuda.html', locals(),
                              context_instance=RequestContext(request))

def catalogo(request):
    return render_to_response('admin/obras/catalogo.html', locals(),
                              context_instance=RequestContext(request))


def c_clasificacion(request):
    return render_to_response('admin/obras/c_clasificacion.html', locals(),
                              context_instance=RequestContext(request))


def c_dependencia(request):
    return render_to_response('admin/obras/c_dependencia.html', locals(),
                              context_instance=RequestContext(request))

def c_subdependencia(request):
    return render_to_response('admin/obras/c_subdependencia.html', locals(),
                              context_instance=RequestContext(request))


def c_impacto(request):
    return render_to_response('admin/obras/c_impacto.html', locals(),
                              context_instance=RequestContext(request))


def c_inaugurador(request):
    return render_to_response('admin/obras/c_inaugurador.html', locals(),
                              context_instance=RequestContext(request))


def c_inversion(request):
    return render_to_response('admin/obras/c_inversion.html', locals(),
                              context_instance=RequestContext(request))


def movimientos(request):
    return render_to_response('admin/obras/movimientos.html', locals(),
                              context_instance=RequestContext(request))


def modifica(request):
    return render_to_response('admin/obras/obra/modifica.html', locals(),
                              context_instance=RequestContext(request))


def consultas(request):
    return render_to_response('admin/obras/consultas.html', locals(),
                              context_instance=RequestContext(request))


def c_filtro(request):
    return render_to_response('admin/obras/c_filtro.html', locals(),
                              context_instance=RequestContext(request))


def c_guardada(request):
    return render_to_response('admin/obras/c_guardada.html', locals(),
                              context_instance=RequestContext(request))


def c_predefinida(request):
    return render_to_response('admin/obras/c_predefinida.html', locals(),
                              context_instance=RequestContext(request))


def usuarios(request):
    return render_to_response('admin/obras/usuarios.html', locals(),
                              context_instance=RequestContext(request))


def is_super_admin(user):
    return user.usuario.rol == 'SA'


@login_required()
@user_passes_test(is_super_admin)
def balance_general(request):
    start_date = datetime.date(2012, 12, 01)
    end_date = datetime.date(2013, 12, 31)
    obras2013 = Obra.objects.filter(
        Q(fechaTermino__range=(start_date, end_date)),
        Q(tipoObra=3)
    )

    total_obras_2013 = obras2013.count()
    total_invertido_2013 = obras2013.aggregate(Sum('inversionTotal'))

    # print 'Total Obras 2013: ' + str(total_obras_2013)
    # print 'Total Invertido 2013: ' + str(total_invertido_2013)

    start_date = datetime.date(2014, 01, 01)
    end_date = datetime.date(2014, 12, 31)
    obras2014 = Obra.objects.filter(
        Q(fechaTermino__range=(start_date, end_date)),
        Q(tipoObra=3)
    )

    total_obras_2014 = obras2014.count()
    total_invertido_2014 = obras2014.aggregate(Sum('inversionTotal'))

    # print 'Total Obras 2014: ' + str(total_obras_2014)
    # print 'Total Invertido 2014: ' + str(total_invertido_2014)

    obras_proceso = Obra.objects.filter(
        Q(tipoObra=2)
    )

    total_obras_proceso = obras_proceso.count()
    total_invertido_proceso = obras_proceso.aggregate(Sum('inversionTotal'))

    # print 'Total Obras Proceso: ' + str(total_obras_proceso)
    # print 'Total Invertido Proceso: ' + str(total_invertido_proceso)

    obras_proyectadas = Obra.objects.filter(
        Q(tipoObra=1)
    )

    total_obras_proyectadas = obras_proyectadas.count()
    total_invertido_proyectadas = obras_proyectadas.aggregate(Sum('inversionTotal'))

    # print 'Total Obras Proyectadas: ' + str(total_obras_proyectadas)
    # print 'Total Invertido Proyectadas: ' + str(total_invertido_proyectadas)

    total_obras = total_obras_2013 + total_obras_2014 + total_obras_proceso + total_obras_proyectadas
    total_invertido = total_invertido_2013.get('inversionTotal__sum') + total_invertido_2014.get(
        'inversionTotal__sum') + total_invertido_proceso.get('inversionTotal__sum') + total_invertido_proyectadas.get(
        'inversionTotal__sum')

    template = loader.get_template('reportes/balance_general.html')
    context = RequestContext(request, {
        'total_obras_2013': total_obras_2013,
        'total_invertido_2013': total_invertido_2013,
        'total_obras_2014': total_obras_2014,
        'total_invertido_2014': total_invertido_2014,
        'total_obras_proceso': total_obras_proceso,
        'total_invertido_proceso': total_invertido_proceso,
        'total_obras_proyectadas': total_obras_proyectadas,
        'total_invertido_proyectadas': total_invertido_proyectadas,
        'total_obras': total_obras,
        'total_invertido': total_invertido,
    })
    return HttpResponse(template.render(context))


@login_required()
@user_passes_test(is_super_admin)
def hipervinculo_informacion_general(request):
    obras_concluidas = Obra.objects.filter(
        Q(tipoObra=3)
    )

    obras_proceso = Obra.objects.filter(
        Q(tipoObra=2)
    )

    obras_proyectadas = Obra.objects.filter(
        Q(tipoObra=1)
    )

    total_obras_proyectadas = obras_proyectadas.count()
    total_obras_proceso = obras_proceso.count()
    total_obras_concluidas = obras_concluidas.count()

    total_invertido_proyectadas = obras_proyectadas.aggregate(Sum('inversionTotal'))
    total_invertido_proceso = obras_proceso.aggregate(Sum('inversionTotal'))
    total_invertido_concluidas = obras_concluidas.aggregate(Sum('inversionTotal'))

    template = loader.get_template('reportes/hipervinculo_informacion_general.html')
    context = RequestContext(request, {
        'total_obras_proyectadas': total_obras_proyectadas,
        'total_obras_proceso': total_obras_proceso,
        'total_obras_concluidas': total_obras_concluidas,
        'total_invertido_proyectadas': total_invertido_proyectadas,
        'total_invertido_proceso': total_invertido_proceso,
        'total_invertido_concluidas': total_invertido_concluidas,
    })
    return HttpResponse(template.render(context))


@login_required()
@user_passes_test(is_super_admin)
def hipervinculo_sector(request):
    start_date_2013 = datetime.date(2012, 12, 01)
    end_date_2013 = datetime.date(2013, 12, 31)

    start_date_2014 = datetime.date(2014, 01, 01)
    end_date_2014 = datetime.date(2014, 12, 31)
    dependencias = {}

    for dependencia in Dependencia.objects.all():
        print dependencia.nombreDependencia

        obras_2013_concluidas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2013, end_date_2013)),
            Q(tipoObra=3),
            Q(dependencia=dependencia),
        )

        obras_2014_concluidas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2014, end_date_2014)),
            Q(tipoObra=3),
            Q(dependencia=dependencia),
        )

        obras_2014_proceso = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2014, end_date_2014)),
            Q(tipoObra=2),
            Q(dependencia=dependencia),
        )

        obras_2014_proyectadas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2014, end_date_2014)),
            Q(tipoObra=1),
            Q(dependencia=dependencia),
        )

        total_obras_concluidas_2013 = obras_2013_concluidas.count()
        total_obras_concluidas_2014 = obras_2014_concluidas.count()
        total_obras_proceso = obras_2014_proceso.count()
        total_obras_proyectadas = obras_2014_proyectadas.count()

        total_invertido_2013 = obras_2013_concluidas.aggregate(Sum('inversionTotal'))
        total_invertido_2014 = obras_2014_concluidas.aggregate(Sum('inversionTotal'))
        total_invertido_proceso = obras_2014_proceso.aggregate(Sum('inversionTotal'))
        total_invertido_proyectadas = obras_2014_proyectadas.aggregate(Sum('inversionTotal'))

        dependencias[dependencia.nombreDependencia] = {}
        dependencias[dependencia.nombreDependencia]['total_obras_concluidas_2013'] = total_obras_concluidas_2013
        dependencias[dependencia.nombreDependencia]['total_obras_concluidas_2014'] = total_obras_concluidas_2014
        dependencias[dependencia.nombreDependencia]['total_obras_proceso'] = total_obras_proceso
        dependencias[dependencia.nombreDependencia]['total_obras_proyectadas'] = total_obras_proyectadas

        dependencias[dependencia.nombreDependencia]['total_invertido_2013'] = total_invertido_2013
        dependencias[dependencia.nombreDependencia]['total_invertido_2014'] = total_invertido_2014
        dependencias[dependencia.nombreDependencia]['total_invertido_proceso'] = total_invertido_proceso
        dependencias[dependencia.nombreDependencia]['total_invertido_proyectadas'] = total_invertido_proyectadas

        print 'total_obras_concluidas_2013: ' + str(total_obras_concluidas_2013)
        print 'total_obras_concluidas_2014: ' + str(total_obras_concluidas_2014)
        print 'total_obras_proceso: ' + str(total_obras_proceso)
        print 'total_obras_proyectadas: ' + str(total_obras_proyectadas)

        print 'total_invertido_2013: ' + str(total_invertido_2013)
        print 'total_invertido_2014: ' + str(total_invertido_2014)
        print 'total_invertido_proceso: ' + str(total_invertido_proceso)
        print 'total_invertido_proyectadas: ' + str(total_invertido_proyectadas)

    template = loader.get_template('reportes/hipervinculo_informacion_sector.html')
    context = RequestContext(request, {
        'dependencias': dependencias,
    })
    print(dependencias)
    return HttpResponse(template.render(context))


@login_required()
@user_passes_test(is_super_admin)
def hipervinculo_entidad(request):
    start_date_2013 = datetime.date(2012, 12, 01)
    end_date_2013 = datetime.date(2013, 12, 31)

    start_date_2014 = datetime.date(2014, 01, 01)
    end_date_2014 = datetime.date(2014, 12, 31)

    start_date_2015 = datetime.date(2015, 01, 01)
    end_date_2015 = datetime.date(2015, 12, 31)

    start_date_2016 = datetime.date(2016, 01, 01)
    end_date_2016 = datetime.date(2016, 12, 31)

    start_date_2017 = datetime.date(2017, 01, 01)
    end_date_2017 = datetime.date(2017, 12, 31)

    start_date_2018 = datetime.date(2018, 01, 01)
    end_date_2018 = datetime.date(2018, 12, 31)
    estados = {}

    for estado in Estado.objects.all():
        print estado.nombreEstado

        obras_2013_concluidas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2013, end_date_2013)),
            Q(tipoObra=3),
            Q(estado=estado),
        )

        obras_2014_concluidas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2014, end_date_2014)),
            Q(tipoObra=3),
            Q(estado=estado),
        )

        obras_proceso = Obra.objects.filter(
            Q(tipoObra=2),
            Q(estado=estado),
        )

        obras_2014_proyectadas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2014, end_date_2014)),
            Q(tipoObra=1),
            Q(estado=estado),
        )

        obras_2015_proyectadas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2015, end_date_2015)),
            Q(tipoObra=1),
            Q(estado=estado),
        )

        obras_2016_proyectadas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2016, end_date_2016)),
            Q(tipoObra=1),
            Q(estado=estado),
        )

        obras_2017_proyectadas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2017, end_date_2017)),
            Q(tipoObra=1),
            Q(estado=estado),
        )

        obras_2018_proyectadas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2018, end_date_2018)),
            Q(tipoObra=1),
            Q(estado=estado),
        )

        total_obras_concluidas_2013 = obras_2013_concluidas.count()
        total_obras_concluidas_2014 = obras_2014_concluidas.count()
        total_obras_proceso = obras_proceso.count()
        total_obras_proyectadas_2014 = obras_2014_proyectadas.count()
        total_obras_proyectadas_2015 = obras_2015_proyectadas.count()
        total_obras_proyectadas_2016 = obras_2016_proyectadas.count()
        total_obras_proyectadas_2017 = obras_2017_proyectadas.count()
        total_obras_proyectadas_2018 = obras_2018_proyectadas.count()

        total_invertido_2013_concluidas = obras_2013_concluidas.aggregate(Sum('inversionTotal'))
        total_invertido_2014_concluidas = obras_2014_concluidas.aggregate(Sum('inversionTotal'))
        total_invertido_proceso = obras_proceso.aggregate(Sum('inversionTotal'))

        total_invertido_proyectadas_2014 = obras_2014_proyectadas.aggregate(Sum('inversionTotal'))
        total_invertido_proyectadas_2015 = obras_2015_proyectadas.aggregate(Sum('inversionTotal'))
        total_invertido_proyectadas_2016 = obras_2016_proyectadas.aggregate(Sum('inversionTotal'))
        total_invertido_proyectadas_2017 = obras_2017_proyectadas.aggregate(Sum('inversionTotal'))
        total_invertido_proyectadas_2018 = obras_2018_proyectadas.aggregate(Sum('inversionTotal'))

        estados[estado.nombreEstado] = {}
        estados[estado.nombreEstado]['total_obras_concluidas_2013'] = total_obras_concluidas_2013
        estados[estado.nombreEstado]['total_obras_concluidas_2014'] = total_obras_concluidas_2014
        estados[estado.nombreEstado]['total_obras_proceso'] = total_obras_proceso
        estados[estado.nombreEstado]['total_obras_proyectadas_2014'] = total_obras_proyectadas_2014
        estados[estado.nombreEstado]['total_obras_proyectadas_2015'] = total_obras_proyectadas_2015
        estados[estado.nombreEstado]['total_obras_proyectadas_2016'] = total_obras_proyectadas_2016
        estados[estado.nombreEstado]['total_obras_proyectadas_2017'] = total_obras_proyectadas_2017
        estados[estado.nombreEstado]['total_obras_proyectadas_2018'] = total_obras_proyectadas_2018

        estados[estado.nombreEstado]['total_invertido_2013_concluidas'] = total_invertido_2013_concluidas
        estados[estado.nombreEstado]['total_invertido_2014_concluidas'] = total_invertido_2014_concluidas
        estados[estado.nombreEstado]['total_invertido_proceso'] = total_invertido_proceso

        estados[estado.nombreEstado]['total_invertido_proyectadas_2014'] = total_invertido_proyectadas_2014
        estados[estado.nombreEstado]['total_invertido_proyectadas_2015'] = total_invertido_proyectadas_2015
        estados[estado.nombreEstado]['total_invertido_proyectadas_2016'] = total_invertido_proyectadas_2016
        estados[estado.nombreEstado]['total_invertido_proyectadas_2017'] = total_invertido_proyectadas_2017
        estados[estado.nombreEstado]['total_invertido_proyectadas_2018'] = total_invertido_proyectadas_2018

    template = loader.get_template('reportes/hipervinculo_entidad.html')
    context = RequestContext(request, {
        'estados': estados,
    })
    return HttpResponse(template.render(context))


@login_required()
@user_passes_test(is_super_admin)
def hipervinculo_concluidas_proceso_proyectadas(request):
    start_date_2013 = datetime.date(2012, 12, 01)
    end_date_2013 = datetime.date(2013, 12, 31)

    start_date_2014 = datetime.date(2014, 01, 01)
    end_date_2014 = datetime.date(2014, 12, 31)

    obras_2013_concluidas = Obra.objects.filter(
        Q(fechaTermino__range=(start_date_2013, end_date_2013)),
        Q(tipoObra=3),
    )

    obras_2014_concluidas = Obra.objects.filter(
        Q(fechaTermino__range=(start_date_2014, end_date_2014)),
        Q(tipoObra=3),
    )

    total_obras_concluidas_2013 = obras_2013_concluidas.count()
    total_invertido_2013_concluidas = obras_2013_concluidas.aggregate(Sum('inversionTotal'))
    total_obras_concluidas_2014 = obras_2014_concluidas.count()
    total_invertido_2014_concluidas = obras_2014_concluidas.aggregate(Sum('inversionTotal'))

    print 'total_obras_concluidas_2013: ' + str(total_obras_concluidas_2013)
    print 'total_invertido_2013_concluidas: ' + str(total_invertido_2013_concluidas)
    print 'total_obras_concluidas_2014: ' + str(total_obras_concluidas_2014)
    print 'total_invertido_2014_concluidas: ' + str(total_invertido_2014_concluidas)

    obras_proceso = Obra.objects.filter(
        Q(tipoObra=2),
    )

    obras_totales_proceso = obras_proceso.count()
    total_invertido_proceso = obras_proceso.aggregate(Sum('inversionTotal'))

    print 'obras_totales_proceso: ' + str(obras_totales_proceso)
    print 'total_invertido_proceso: ' + str(total_invertido_proceso)

    obras_proyectadas = Obra.objects.filter(
        Q(tipoObra=1),
    )

    obras_totales_proyectadas = obras_proyectadas.count()
    total_invertido_proyectadas = obras_proyectadas.aggregate(Sum('inversionTotal'))

    print 'obras_totales_proyectadas: ' + str(obras_totales_proyectadas)
    print 'total_invertido_proyectadas: ' + str(total_invertido_proyectadas)

    template = loader.get_template('reportes/hipervinculo_concluidas_proceso_proyectadas.html')
    context = RequestContext(request, {
        'total_obras_concluidas_2013': total_obras_concluidas_2013,
        'total_invertido_2013_concluidas': total_invertido_2013_concluidas,
        'total_obras_concluidas_2014': total_obras_concluidas_2014,
        'total_invertido_2014_concluidas': total_invertido_2014_concluidas,
        'obras_totales_proceso': obras_totales_proceso,
        'total_invertido_proceso': total_invertido_proceso,
        'obras_totales_proyectadas': obras_totales_proyectadas,
        'total_invertido_proyectadas': total_invertido_proyectadas,
    })
    return HttpResponse(template.render(context))


@login_required()
def consulta_web(request):

    if request.user.usuario.rol == 'SA':
        dependencias = Dependencia.objects.all()
    elif request.user.usuario.rol == 'AD':
        dependencias = Dependencia.objects.filter(
                Q(id=request.user.usuario.dependencia.id) |
                Q(dependienteDe__id=request.user.usuario.dependencia.id))
    elif request.user.usuario.rol == 'US':
        dependencias = Dependencia.objects.filter(
                    Q(id=request.user.usuario.dependencia.id)
                    )
    #templates = loader.get_template('consultas/busqueda_general.html')
    template = loader.get_template('admin/obras/consulta_filtros/consulta-filtros.html')
    context = RequestContext(request, {
        'estatusObra': TipoObra.objects.all(),
        'dependencias': dependencias,
        'estados': Estado.objects.all(),
        'tipo_inversiones': TipoInversion.objects.all(),
        'impactos': Impacto.objects.all(),
        'clasificacion': TipoClasificacion.objects.all(),
        'inaugurador': Inaugurador.objects.all(),
        'InstanciaEjecutora': InstanciaEjecutora.objects.all(),
    })
    return HttpResponse(template.render(context))


def get_array_or_none(the_string):
    if the_string is None:
        return None
    else:
        return map(int, the_string.split(','))


def buscar_obras_web(request):
    #TODO cambiar los parametros 'None' por get del request
    buscador = BuscarObras(
            idtipoobra=get_array_or_none(request.GET.get('tipoDeObra')),
            iddependencias=get_array_or_none(request.GET.get('dependencia')),
            estados=get_array_or_none(request.GET.get('estado')),
            clasificaciones=get_array_or_none(request.GET.get('clasificacion')),
            inversiones=get_array_or_none(request.GET.get('tipoDeInversion')),
            inauguradores=get_array_or_none(request.GET.get('inaugurador')),
            impactos=get_array_or_none(request.GET.get('impacto')),
            inaugurada=request.GET.get('inaugurada', None),
            inversion_minima=request.GET.get('inversionMinima', None),
            inversion_maxima=request.GET.get('inversionMaxima', None),
            fecha_inicio_primera=request.GET.get('fechaInicio', None),
            fecha_inicio_segunda=request.GET.get('fechaInicio', None),
            fecha_fin_primera=request.GET.get('fechaFin', None),
            fecha_fin_segunda=request.GET.get('fechaFinSegunda', None),
            denominacion=request.GET.get('denominacion', None),
            instancia_ejecutora=get_array_or_none(request.GET.get('instanciaEjecutora')),

    )
    resultados = buscador.buscar()

    template = loader.get_template('admin/obras/consulta_filtros/consulta-filtros.html')
    context = RequestContext(request, {
        'resultados': resultados,
        'filtros': request.GET
    })
    return HttpResponse(template.render(context))


def obras_iniciadas(request):
    usuario = request.user.usuario

    query = Q(fechaInicio__lte= datetime.datetime.now().date())
    if not (usuario.rol == 'SA'):
        subdependencias = get_subdependencias_as_list_flat(usuario.dependencia)
        query = query & (Q(dependencia__in=subdependencias) | Q(subdependencia__in=subdependencias))
    obras = Obra.objects.filter(query)

    template = loader.get_template('admin/obras/consulta_predefinidos/consulta-predefinidos.html')
    context = RequestContext(request, {
        'obras_resultado': obras
    })
    return HttpResponse(template.render(context))


def obras_vencidas(request):
    usuario = request.user.usuario

    today = datetime.datetime.now().date()
    if usuario.rol == 'SA':
        obras = Obra.objects.filter(fechaTermino__lte=today)
    else:
        obras = Obra.objects.filter(Q(fechaTermino__lte=today) & Q(
            dependencia__in=get_subdependencias_as_list_flat(usuario.dependencia)))

    template = loader.get_template('admin/obras/consulta_predefinidos/consulta-predefinidos.html')
    context = RequestContext(request, {
        'obras_resultado': obras
    })
    return HttpResponse(template.render(context))


def obras_for_dependencia(request):
    usuario = request.user.usuario

    if usuario.rol == 'SA':
        obras = Obra.objects.all()
    else:
        obras = usuario.dependencia.get_obras()

    template = loader.get_template('admin/obras/consulta_predefinidos/consulta-predefinidos.html')
    context = RequestContext(request, {
        'obras_resultado': obras
    })
    return HttpResponse(template.render(context))


def ajax_prueba(request):
    template = loader.get_template('prueba.html')
    return HttpResponse(template.render(RequestContext(request)))




# reportes de power point ************************************************************************************

def fichaTecnica(request):
        prs = Presentation('obras/static/ppt/FichaTecnicaObras.pptx')
        usuario = request.user.usuario
        buscador = BuscaObra(
            identificador_unico=request.GET.get('identificador_unico', None)
        )
        resultados = buscador.busca()

        json_map = {}
        json_map['obras'] = []
        for obra in resultados['obras']:
            json_map['obras'].append(obra.to_serializable_dict())

        json_map['DInversion'] = []
        for DetalleInversion in resultados['DInversion']:
            json_map['DInversion'].append(DetalleInversion.to_serializable_dict())

        prs.slides[0].shapes[9].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[9].text = json_map['obras'][0]['identificador']
        prs.slides[0].shapes[10].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[10].text = json_map['obras'][0]['denominacion']
        prs.slides[0].shapes[11].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[11].text = json_map['obras'][0]['dependencia']['nombreDependencia']
        prs.slides[0].shapes[12].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[12].text = json_map['obras'][0]['estado']['nombreEstado']
        prs.slides[0].shapes[13].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[13].text = json_map['obras'][0]['municipio']
        prs.slides[0].shapes[14].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[14].text = json_map['obras'][0]['fechaInicio']
        prs.slides[0].shapes[15].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[15].text = json_map['obras'][0]['fechaTermino']
        prs.slides[0].shapes[16].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[16].text = json_map['obras'][0]['tipoObra']['nombreTipoObra']

        prs.slides[0].shapes[17].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[17].text = str(json_map['obras'][0]['porcentajeAvance'])
        prs.slides[0].shapes[18].text_frame.paragraphs[0].font.size = Pt(8)
        prs.slides[0].shapes[18].text = json_map['obras'][0]['fechaModificacion']

        for DI in json_map['DInversion']:
            if not (DI['tipoInversion'] is None):
                if DI['tipoInversion'] == 1:
                    prs.slides[0].shapes[19].text_frame.paragraphs[0].font.size = Pt(8)
                    prs.slides[0].shapes[19].text = "Si"
                if DI['tipoInversion'] == 2:
                    prs.slides[0].shapes[20].text_frame.paragraphs[0].font.size = Pt(8)
                    prs.slides[0].shapes[20].text = "Si"


        prs.save('obras/static/ppt/ppt-generados/FichaTecnicaObras_' + str(usuario.user.id) + '.pptx')
        print(json_map)
        return HttpResponse(json.dumps(json_map), 'application/json')

def reportes_predefinidos(request):
    return render_to_response('admin/obras/consulta_predefinidos/consulta-predefinidos.html', {'clases': ''}, context_instance=RequestContext(request))

def abrir_pptx(archivo):
    f = os.popen(archivo,'r')
    prs = Presentation(f)
    f.close()

@login_required()
@user_passes_test(is_super_admin)
def balance_general_ppt(request):
    prs = Presentation('obras/static/ppt/PRINCIPAL_BALANCE_GENERAL_APF.pptx')
    usuario = request.user.usuario
    # informacion para el 2013
    start_date = datetime.date(2012, 12, 01)
    end_date = datetime.date(2013, 12, 31)
    obras2013 = Obra.objects.filter(
        Q(fechaTermino__range=(start_date, end_date)),
        Q(tipoObra=3)
    )

    total_obras_2013 = obras2013.count()
    total_invertido_2013 = obras2013.aggregate(Sum('inversionTotal'))

    # informacion para el 2014
    start_date = datetime.date(2014, 01, 01)
    end_date = datetime.date(2014, 12, 31)
    obras2014 = Obra.objects.filter(
        Q(fechaTermino__range=(start_date, end_date)),
        Q(tipoObra=3)
    )

    total_obras_2014 = obras2014.count()
    total_invertido_2014 = obras2014.aggregate(Sum('inversionTotal'))

    # informacion para obras en proceso
    obras_proceso = Obra.objects.filter(
        Q(tipoObra=2)
    )

    total_obras_proceso = obras_proceso.count()
    total_invertido_proceso = obras_proceso.aggregate(Sum('inversionTotal'))

    # informacion para obras proyectadas
    obras_proyectadas = Obra.objects.filter(
        Q(tipoObra=1)
    )

    total_obras_proyectadas = obras_proyectadas.count()
    total_invertido_proyectadas = obras_proyectadas.aggregate(Sum('inversionTotal'))

    # informacion para obras totales
    total_obras = total_obras_2013 + total_obras_2014 + total_obras_proceso + total_obras_proyectadas
    total_invertido = total_invertido_2013.get('inversionTotal__sum',0) + total_invertido_2014.get(
        'inversionTotal__sum',0) + total_invertido_proceso.get('inversionTotal__sum',0) + total_invertido_proyectadas.get(
        'inversionTotal__sum',0)


    prs.slides[0].shapes[15].text= '{0:,}'.format(total_obras_2013)
    prs.slides[0].shapes[16].text= '$ {0:,.2f}'.format(total_invertido_2013.get('inversionTotal__sum',0))
    prs.slides[0].shapes[17].text= '{0:,}'.format(total_obras_2014)
    prs.slides[0].shapes[18].text= '$ {0:,.2f}'.format(total_invertido_2014.get('inversionTotal__sum',0))
    prs.slides[0].shapes[21].text= '{0:,}'.format(total_obras_proceso)
    prs.slides[0].shapes[22].text= '$ {0:,.2f}'.format(total_invertido_proceso.get('inversionTotal__sum',0))
    prs.slides[0].shapes[23].text= '{0:,}'.format(total_obras_proyectadas)
    prs.slides[0].shapes[24].text= '$ {0:,.2f}'.format(total_invertido_proyectadas.get('inversionTotal__sum',0))
    prs.slides[0].shapes[19].text= '{0:,}'.format(total_obras)
    prs.slides[0].shapes[20].text= '$ {0:,.2f}'.format(total_invertido)


    prs.save('obras/static/ppt/ppt-generados/balance_general_' + str(usuario.user.id) + '.pptx')

    the_file = 'obras/static/ppt/ppt-generados/balance_general_' + str(usuario.user.id) + '.pptx'
    filename = os.path.basename(the_file)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(the_file,"rb"), chunk_size),
                           content_type=mimetypes.guess_type(the_file)[0])
    response['Content-Length'] = os.path.getsize(the_file)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response



@login_required()
@user_passes_test(is_super_admin)
def hiper_info_general_ppt(request):
    prs = Presentation('obras/static/ppt/HIPERVINCULO_INFORMACION_GENERAL.pptx')
    usuario = request.user.usuario
    obras_concluidas = Obra.objects.filter(
        Q(tipoObra=3)
    )

    obras_proceso = Obra.objects.filter(
        Q(tipoObra=2)
    )

    obras_proyectadas = Obra.objects.filter(
        Q(tipoObra=1)
    )

    total_obras_proyectadas = obras_proyectadas.count()
    total_obras_proceso = obras_proceso.count()
    total_obras_concluidas = obras_concluidas.count()

    total_invertido_proyectadas = obras_proyectadas.aggregate(Sum('inversionTotal'))
    total_invertido_proceso = obras_proceso.aggregate(Sum('inversionTotal'))
    total_invertido_concluidas = obras_concluidas.aggregate(Sum('inversionTotal'))

    prs.slides[0].shapes[3].text= '{0:,}'.format(total_obras_concluidas)
    prs.slides[0].shapes[4].text= '$ {0:,.2f}'.format(total_invertido_concluidas.get('inversionTotal__sum',0))
    prs.slides[1].shapes[3].text= '{0:,}'.format(total_obras_proceso)
    prs.slides[1].shapes[4].text= '$ {0:,.2f}'.format(total_invertido_proceso.get('inversionTotal__sum',0))
    prs.slides[2].shapes[3].text= '{0:,}'.format(total_obras_proyectadas)
    prs.slides[2].shapes[4].text= '$ {0:,.2f}'.format(total_invertido_proyectadas.get('inversionTotal__sum',0))



    prs.save('obras/static/ppt/ppt-generados/hiper_info_general_' + str(usuario.user.id) + '.pptx')

    the_file = 'obras/static/ppt/ppt-generados/hiper_info_general_' + str(usuario.user.id) + '.pptx'
    filename = os.path.basename(the_file)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(the_file,"rb"), chunk_size),
                           content_type=mimetypes.guess_type(the_file)[0])
    response['Content-Length'] = os.path.getsize(the_file)
    response['Content-Disposition'] = "attachment; filename=%s" % filename

    return response
    #abrir_pptx('hiper_info_general.pptx')
    #return render_to_response('admin/obras/consulta_predefinidos/consulta-predefinidos.html', {'clases': ''}, context_instance=RequestContext(request))

@login_required()
@user_passes_test(is_super_admin)
def hiper_inauguradas_ppt(request):
    prs = Presentation('obras/static/ppt/HIPERVINCULO_INAUGURADAS_SENALIZADAS.pptx')
    usuario = request.user.usuario
    # falta implementar

    prs.save('obras/static/ppt/ppt-generados/hiper_inauguradas_' + str(usuario.user.id) + '.pptx')

    the_file = 'obras/static/ppt/ppt-generados/hiper_inauguradas_' + str(usuario.user.id) + '.pptx'
    filename = os.path.basename(the_file)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(the_file,"rb"), chunk_size),
                           content_type=mimetypes.guess_type(the_file)[0])
    response['Content-Length'] = os.path.getsize(the_file)
    response['Content-Disposition'] = "attachment; filename=%s" % filename

    return response

@login_required()
@user_passes_test(is_super_admin)
def hiper_por_sector_ppt(request):
    prs = Presentation('obras/static/ppt/HIPERVINCULO_POR_SECTOR.pptx')
    usuario = request.user.usuario
    start_date_2013 = datetime.date(2012, 12, 01)
    end_date_2013 = datetime.date(2013, 12, 31)

    start_date_2014 = datetime.date(2014, 01, 01)
    end_date_2014 = datetime.date(2014, 12, 31)
    dependencias = {}

    for dependencia in Dependencia.objects.filter(
        Q(obraoprograma='O')
    ):
        print dependencia.nombreDependencia

        obras_2013_concluidas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2013, end_date_2013)),
            Q(tipoObra=3),
            Q(dependencia=dependencia),
        )

        obras_2014_concluidas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2014, end_date_2014)),
            Q(tipoObra=3),
            Q(dependencia=dependencia),
        )

        obras_2014_proceso = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2014, end_date_2014)),
            Q(tipoObra=2),
            Q(dependencia=dependencia),
        )

        obras_2014_proyectadas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2014, end_date_2014)),
            Q(tipoObra=1),
            Q(dependencia=dependencia),
        )

        total_obras_concluidas_2013 = obras_2013_concluidas.count()
        total_obras_concluidas_2014 = obras_2014_concluidas.count()
        total_obras_proceso = obras_2014_proceso.count()
        total_obras_proyectadas = obras_2014_proyectadas.count()

        total_invertido_2013 = obras_2013_concluidas.aggregate(Sum('inversionTotal'))
        total_invertido_2014 = obras_2014_concluidas.aggregate(Sum('inversionTotal'))
        total_invertido_proceso = obras_2014_proceso.aggregate(Sum('inversionTotal'))
        total_invertido_proyectadas = obras_2014_proyectadas.aggregate(Sum('inversionTotal'))



        if dependencia.nombreDependencia =='SEGOB': indiceSlide =0
        elif dependencia.nombreDependencia =='SEDESOL': indiceSlide =4
        elif dependencia.nombreDependencia =='SEMARNAT': indiceSlide = 8
        elif dependencia.nombreDependencia =='SAGARPA': indiceSlide = 12
        elif dependencia.nombreDependencia =='SCT': indiceSlide = 16
        elif dependencia.nombreDependencia =='SEP': indiceSlide = 20
        elif dependencia.nombreDependencia =='SS': indiceSlide = 24
        elif dependencia.nombreDependencia =='SEDATU': indiceSlide = 28
        elif dependencia.nombreDependencia =='SECTUR': indiceSlide = 32
        elif dependencia.nombreDependencia =='PEMEX': indiceSlide = 36
        elif dependencia.nombreDependencia =='CFE': indiceSlide = 40
        elif dependencia.nombreDependencia =='IMSS': indiceSlide = 44
        elif dependencia.nombreDependencia =='ISSSTE': indiceSlide = 48
        elif dependencia.nombreDependencia =='CONAGUA': indiceSlide = 52
        else: indiceSlide =56

        totalinvertidoproceso=0
        totalinvertido2013=0
        totalinvertido2014=0
        totalinvertidoproyectadas=0
        if str(total_invertido_2013.get('inversionTotal__sum',0)) != 'None': totalinvertido2013=total_invertido_2013.get('inversionTotal__sum',0)
        if str(total_invertido_2014.get('inversionTotal__sum',0)) != 'None': totalinvertido2014=total_invertido_2014.get('inversionTotal__sum',0)
        if str(total_invertido_proyectadas.get('inversionTotal__sum',0)) != 'None': totalinvertidoproyectadas=total_invertido_proyectadas.get('inversionTotal__sum',0)
        if str(total_invertido_proceso.get('inversionTotal__sum',0)) != 'None': totalinvertidoproceso=total_invertido_proceso.get('inversionTotal__sum',0)

        TOTAL_INVERTIDO=totalinvertido2013+totalinvertido2014+totalinvertidoproceso+totalinvertidoproyectadas
        TOTAL_OBRAS=total_obras_concluidas_2013+total_obras_concluidas_2014+total_obras_proceso+total_obras_proyectadas

        prs.slides[indiceSlide].shapes[5].text= '{0:,}'.format(total_obras_concluidas_2013)
        prs.slides[indiceSlide].shapes[6].text= '$ {0:,.2f}'.format(totalinvertido2013)
        prs.slides[indiceSlide].shapes[7].text= '{0:,}'.format(total_obras_concluidas_2014)
        prs.slides[indiceSlide].shapes[8].text= '$ {0:,.2f}'.format(totalinvertido2014)
        prs.slides[indiceSlide].shapes[9].text= '{0:,}'.format(TOTAL_OBRAS)
        prs.slides[indiceSlide].shapes[10].text= '$ {0:,.2f}'.format(TOTAL_INVERTIDO)
        prs.slides[indiceSlide].shapes[11].text= '{0:,}'.format(total_obras_proceso)
        prs.slides[indiceSlide].shapes[12].text= '$ {0:,.2f}'.format(totalinvertidoproceso)
        prs.slides[indiceSlide].shapes[13].text= '{0:,}'.format(total_obras_proyectadas)
        prs.slides[indiceSlide].shapes[14].text= '$ {0:,.2f}'.format(totalinvertidoproyectadas)



    prs.save('obras/static/ppt/ppt-generados/hiper_por_sector_' + str(usuario.user.id) + '.pptx')

    the_file = 'obras/static/ppt/ppt-generados/hiper_por_sector_' + str(usuario.user.id) + '.pptx'
    filename = os.path.basename(the_file)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(the_file,"rb"), chunk_size),
                           content_type=mimetypes.guess_type(the_file)[0])
    response['Content-Length'] = os.path.getsize(the_file)
    response['Content-Disposition'] = "attachment; filename=%s" % filename

    return response
@login_required()
@user_passes_test(is_super_admin)
def hiper_por_entidad_ppt(request):
    prs = Presentation('obras/static/ppt/HIPERVINCULOS_POR_ENTIDAD.pptx')
    usuario = request.user.usuario
    start_date_2013 = datetime.date(2012, 12, 01)
    end_date_2013 = datetime.date(2013, 12, 31)

    start_date_2014 = datetime.date(2014, 01, 01)
    end_date_2014 = datetime.date(2014, 12, 31)

    start_date_2015 = datetime.date(2015, 01, 01)
    end_date_2015 = datetime.date(2015, 12, 31)

    start_date_2016 = datetime.date(2016, 01, 01)
    end_date_2016 = datetime.date(2016, 12, 31)

    start_date_2017 = datetime.date(2017, 01, 01)
    end_date_2017 = datetime.date(2017, 12, 31)

    start_date_2018 = datetime.date(2018, 01, 01)
    end_date_2018 = datetime.date(2018, 12, 31)
    indiceSlide=0
    estados = {}
    listaEstados = Estado.objects.exclude(nombreEstado='INTERESTATAL').exclude(nombreEstado='NACIONAL')
    listaEstados = listaEstados.order_by('nombreEstado')

    for estado in listaEstados:
        print estado.nombreEstado

        obras_2013_concluidas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2013, end_date_2013)),
            Q(tipoObra=3),
            Q(estado=estado),
        )

        obras_2014_concluidas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2014, end_date_2014)),
            Q(tipoObra=3),
            Q(estado=estado),
        )

        obras_proceso = Obra.objects.filter(
            Q(tipoObra=2),
            Q(estado=estado),
        )

        obras_2014_proyectadas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2014, end_date_2014)),
            Q(tipoObra=1),
            Q(estado=estado),
        )

        obras_2015_proyectadas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2015, end_date_2015)),
            Q(tipoObra=1),
            Q(estado=estado),
        )

        obras_2016_proyectadas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2016, end_date_2016)),
            Q(tipoObra=1),
            Q(estado=estado),
        )

        obras_2017_proyectadas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2017, end_date_2017)),
            Q(tipoObra=1),
            Q(estado=estado),
        )

        obras_2018_proyectadas = Obra.objects.filter(
            Q(fechaTermino__range=(start_date_2018, end_date_2018)),
            Q(tipoObra=1),
            Q(estado=estado),
        )

        total_obras_concluidas_2013 = obras_2013_concluidas.count()
        total_obras_concluidas_2014 = obras_2014_concluidas.count()
        total_obras_proceso = obras_proceso.count()
        total_obras_proyectadas_2014 = obras_2014_proyectadas.count()
        total_obras_proyectadas_2015 = obras_2015_proyectadas.count()
        total_obras_proyectadas_2016 = obras_2016_proyectadas.count()
        total_obras_proyectadas_2017 = obras_2017_proyectadas.count()
        total_obras_proyectadas_2018 = obras_2018_proyectadas.count()

        total_invertido_2013_concluidas = obras_2013_concluidas.aggregate(Sum('inversionTotal'))
        total_invertido_2014_concluidas = obras_2014_concluidas.aggregate(Sum('inversionTotal'))
        total_invertido_proceso = obras_proceso.aggregate(Sum('inversionTotal'))

        total_invertido_proyectadas_2014 = obras_2014_proyectadas.aggregate(Sum('inversionTotal'))
        total_invertido_proyectadas_2015 = obras_2015_proyectadas.aggregate(Sum('inversionTotal'))
        total_invertido_proyectadas_2016 = obras_2016_proyectadas.aggregate(Sum('inversionTotal'))
        total_invertido_proyectadas_2017 = obras_2017_proyectadas.aggregate(Sum('inversionTotal'))
        total_invertido_proyectadas_2018 = obras_2018_proyectadas.aggregate(Sum('inversionTotal'))

        totalinvertido2013=0
        totalinvertido2014=0
        totalinvertidoproceso=0
        totalinvertidoproyectadas2014=0
        totalinvertidoproyectadas2015=0
        totalinvertidoproyectadas2016=0
        totalinvertidoproyectadas2017=0
        totalinvertidoproyectadas2018=0

        if str(total_invertido_2013_concluidas.get('inversionTotal__sum',0)) != 'None': totalinvertido2013=total_invertido_2013_concluidas.get('inversionTotal__sum',0)
        if str(total_invertido_2014_concluidas.get('inversionTotal__sum',0)) != 'None': totalinvertido2014=total_invertido_2014_concluidas.get('inversionTotal__sum',0)
        if str(total_invertido_proceso.get('inversionTotal__sum',0)) != 'None': totalinvertidoproceso=total_invertido_proceso.get('inversionTotal__sum',0)
        if str(total_invertido_proyectadas_2014.get('inversionTotal__sum',0)) != 'None': totalinvertidoproyectadas2014=total_invertido_proyectadas_2014.get('inversionTotal__sum',0)
        if str(total_invertido_proyectadas_2015.get('inversionTotal__sum',0)) != 'None': totalinvertidoproyectadas2015=total_invertido_proyectadas_2015.get('inversionTotal__sum',0)
        if str(total_invertido_proyectadas_2016.get('inversionTotal__sum',0)) != 'None': totalinvertidoproyectadas2016=total_invertido_proyectadas_2016.get('inversionTotal__sum',0)
        if str(total_invertido_proyectadas_2017.get('inversionTotal__sum',0)) != 'None': totalinvertidoproyectadas2017=total_invertido_proyectadas_2017.get('inversionTotal__sum',0)
        if str(total_invertido_proyectadas_2018.get('inversionTotal__sum',0)) != 'None': totalinvertidoproyectadas2018=total_invertido_proyectadas_2018.get('inversionTotal__sum',0)

        totalObras14_18 = totalinvertidoproyectadas2014+totalinvertidoproyectadas2015+totalinvertidoproyectadas2016+totalinvertidoproyectadas2017+totalinvertidoproyectadas2018
        totalInvertido14_18 = total_obras_proyectadas_2014+total_obras_proyectadas_2015+total_obras_proyectadas_2016+total_obras_proyectadas_2017+total_obras_proyectadas_2018

        totalObrasGeneral = totalObras14_18+total_obras_concluidas_2013+total_obras_concluidas_2014+total_obras_proceso
        totalInvertidoGeneral = totalInvertido14_18+totalinvertido2013+totalinvertido2014+totalinvertidoproceso

        prs.slides[indiceSlide].shapes[9].text= '{0:,}'.format(total_obras_concluidas_2013)
        prs.slides[indiceSlide].shapes[10].text= '$ {0:,.2f}'.format(totalinvertido2013)
        prs.slides[indiceSlide].shapes[11].text= '{0:,}'.format(total_obras_concluidas_2014)
        prs.slides[indiceSlide].shapes[12].text= '$ {0:,.2f}'.format(totalinvertido2014)
        prs.slides[indiceSlide].shapes[13].text= '{0:,}'.format(total_obras_proceso)
        prs.slides[indiceSlide].shapes[14].text= '$ {0:,.2f}'.format(totalinvertidoproceso)
        prs.slides[indiceSlide].shapes[15].text= 'min1'
        prs.slides[indiceSlide].shapes[16].text= 'min2'
        prs.slides[indiceSlide].shapes[17].text= 'max1'
        prs.slides[indiceSlide].shapes[18].text= 'max2'

        prs.slides[indiceSlide].shapes[19].text= '{0:,}'.format(total_obras_proyectadas_2014)
        prs.slides[indiceSlide].shapes[20].text= '$ {0:,.2f}'.format(totalinvertidoproyectadas2014)
        prs.slides[indiceSlide].shapes[21].text= '{0:,}'.format(total_obras_proyectadas_2015)
        prs.slides[indiceSlide].shapes[22].text= '$ {0:,.2f}'.format(totalinvertidoproyectadas2015)
        prs.slides[indiceSlide].shapes[23].text= '{0:,}'.format(total_obras_proyectadas_2016)
        prs.slides[indiceSlide].shapes[24].text= '$ {0:,.2f}'.format(totalinvertidoproyectadas2016)
        prs.slides[indiceSlide].shapes[25].text= '{0:,}'.format(total_obras_proyectadas_2017)
        prs.slides[indiceSlide].shapes[26].text= '$ {0:,.2f}'.format(totalinvertidoproyectadas2017)
        prs.slides[indiceSlide].shapes[27].text= '{0:,}'.format(total_obras_proyectadas_2018)
        prs.slides[indiceSlide].shapes[28].text= '$ {0:,.2f}'.format(totalinvertidoproyectadas2018)
        prs.slides[indiceSlide].shapes[29].text= '{0:,}'.format(totalObras14_18)
        prs.slides[indiceSlide].shapes[30].text= '$ {0:,.2f}'.format(totalInvertido14_18)
        prs.slides[indiceSlide].shapes[31].text= '{0:,}'.format(totalObrasGeneral)
        #prs.slides[indiceSlide].shapes[32].text= '$ {0:,.2f}'.format(totalInvertidoGeneral)

        indiceSlide=indiceSlide+1


    prs.save('obras/static/ppt/ppt-generados/hiper_por_entidad_' + str(usuario.user.id) + '.pptx')

    the_file = 'obras/static/ppt/ppt-generados/hiper_por_entidad_' + str(usuario.user.id) + '.pptx'
    filename = os.path.basename(the_file)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(the_file,"rb"), chunk_size),
                           content_type=mimetypes.guess_type(the_file)[0])
    response['Content-Length'] = os.path.getsize(the_file)
    response['Content-Disposition'] = "attachment; filename=%s" % filename

    return response