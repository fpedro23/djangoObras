# Create your views here.
import datetime
import json
from django.shortcuts import render_to_response
import os
from django.forms import model_to_dict
import json
from django.forms import model_to_dict
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test
from oauth2_provider.views import ProtectedResourceView
from oauth2_provider.models import AccessToken

# from pptx import Presentation
from obras.models import *
from obras.BuscarObras import BuscarObras
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
import json
from obras.models import Obra
from django.contrib.auth.models import User
import datetime
from obras.BuscarObras import BuscarObras
from django.shortcuts import render_to_response


class HoraEndpoint(ProtectedResourceView):

    def get(self, request):
        json_response = {}
        date = datetime.datetime.now()
        time = date.time()

        json_response['dia'] = date.day
        json_response['mes'] = date.month
        json_response['ano'] = date.year

        json_response['hora'] = time.hour
        json_response['minuto'] = time.minute
        json_response['segundo'] = time.second

        return HttpResponse(json.dumps(json_response), 'application/json')


class ObrasIniciadasEndpoint(ProtectedResourceView):

    def get(self, request):
        json_response = []
        today = datetime.datetime.now().date()

        obras = Obra.objects.filter(Q(fechaInicio__lte=today)).all()

        for obra in obras:
            map = {}

            map['identificador'] = obra.identificador_unico
            map['tipoObra'] = obra.tipoObra.to_serializable_dict()
            map['dependencia'] = obra.dependencia.to_serializable_dict()
            map['estado'] = obra.estado.to_serializable_dict()
            map['impacto'] = obra.impacto.to_serializable_dict()

            map['tipoInversion'] = []
            for tipoInversion in obra.tipoInversion.all():
                tipo = tipoInversion.to_serializable_dict()
                map['tipoInversion'].append(tipo)

            map['tipoClasificacion'] = []
            for tipoClasificacion in obra.tipoClasificacion.all():
                tipo = tipoClasificacion.to_serializable_dict()
                map['tipoClasificacion'].append(tipo)

            map['inaugurador'] = obra.inaugurador.to_serializable_dict()
            map['registroHacendario'] = obra.registroHacendario
            map['registroAuditoria'] = obra.registroAuditoria
            map['denominacion'] = obra.denominacion
            map['descripcion'] = obra.descripcion
            map['observaciones'] = obra.observaciones
            if obra.fechaInicio is None:
                map['fechaInicio'] = None
            else:
                map['fechaInicio'] = obra.fechaInicio.__str__()
            if obra.fechaTermino is None:
                map['fechaTermino'] = None
            else:
                map['fechaTermino'] = obra.fechaTermino.__str__()
            if obra.inversionTotal is None:
                map['inversionTotal'] = 0.0
            else:
                map['inversionTotal'] = float(obra.inversionTotal)
            if obra.totalBeneficiarios is None:
                map['totalBeneficiarios'] = 0
            else:
                map['totalBeneficiarios'] = int(obra.totalBeneficiarios)
            map['senalizacion'] = obra.senalizacion
            map['susceptibleInauguracion'] = obra.susceptibleInauguracion
            if obra.porcentajeAvance is None:
                map['porcentajeAvance'] = 0.0
            else:
                map['porcentajeAvance'] = float(obra.porcentajeAvance)
            if obra.fotoAntes is None:
                map['fotoAntes'] = None
            else:
                map['fotoAntes'] = obra.fotoAntes.name
            if obra.fotoDurante is None:
                map['fotoAntes'] = None
            else:
                map['fotoAntes'] = obra.fotoDurante.name
            if obra.fotoDespues is None:
                map['fotoAntes'] = None
            else:
                map['fotoAntes'] = obra.fotoDespues.name
            map['inaugurada'] = obra.inaugurada
            map['poblacionObjetivo'] = obra.poblacionObjetivo
            map['municipio'] = obra.municipio
            if obra.tipoMoneda is None:
                map['tipoMoneda'] = None
            else:
                map['tipoMoneda'] = obra.tipoMoneda.to_serializable_dict()

            json_response.append(map)

        return HttpResponse(json.dumps(json_response), 'application/json')


class ObrasVencidasEndpoint(ProtectedResourceView):

    def get(self, request):
        json_response = []
        today = datetime.datetime.now().date()

        obras = Obra.objects.filter(Q(fechaTermino__lte=today))

        for obra in obras:
            map = {}

            map['identificador'] = obra.identificador_unico
            map['tipoObra'] = obra.tipoObra.to_serializable_dict()
            map['dependencia'] = obra.dependencia.to_serializable_dict()
            map['estado'] = obra.estado.to_serializable_dict()
            map['impacto'] = obra.impacto.to_serializable_dict()

            map['tipoInversion'] = []
            for tipoInversion in obra.tipoInversion.all():
                tipo = tipoInversion.to_serializable_dict()
                map['tipoInversion'].append(tipo)

            map['tipoClasificacion'] = []
            for tipoClasificacion in obra.tipoClasificacion.all():
                tipo = tipoClasificacion.to_serializable_dict()
                map['tipoClasificacion'].append(tipo)

            map['inaugurador'] = obra.inaugurador.to_serializable_dict()
            map['registroHacendario'] = obra.registroHacendario
            map['registroAuditoria'] = obra.registroAuditoria
            map['denominacion'] = obra.denominacion
            map['descripcion'] = obra.descripcion
            map['observaciones'] = obra.observaciones
            if obra.fechaInicio is None:
                map['fechaInicio'] = None
            else:
                map['fechaInicio'] = obra.fechaInicio.__str__()
            if obra.fechaTermino is None:
                map['fechaTermino'] = None
            else:
                map['fechaTermino'] = obra.fechaTermino.__str__()
            if obra.inversionTotal is None:
                map['inversionTotal'] = 0.0
            else:
                map['inversionTotal'] = float(obra.inversionTotal)
            if obra.totalBeneficiarios is None:
                map['totalBeneficiarios'] = 0
            else:
                map['totalBeneficiarios'] = int(obra.totalBeneficiarios)
            map['senalizacion'] = obra.senalizacion
            map['susceptibleInauguracion'] = obra.susceptibleInauguracion
            if obra.porcentajeAvance is None:
                map['porcentajeAvance'] = 0.0
            else:
                map['porcentajeAvance'] = float(obra.porcentajeAvance)
            if obra.fotoAntes is None:
                map['fotoAntes'] = None
            else:
                map['fotoAntes'] = obra.fotoAntes.name
            if obra.fotoDurante is None:
                map['fotoAntes'] = None
            else:
                map['fotoAntes'] = obra.fotoDurante.name
            if obra.fotoDespues is None:
                map['fotoAntes'] = None
            else:
                map['fotoAntes'] = obra.fotoDespues.name
            map['inaugurada'] = obra.inaugurada
            map['poblacionObjetivo'] = obra.poblacionObjetivo
            map['municipio'] = obra.municipio
            if obra.tipoMoneda is None:
                map['tipoMoneda'] = None
            else:
                map['tipoMoneda'] = obra.tipoMoneda.to_serializable_dict()

            json_response.append(map)

        return HttpResponse(json.dumps(json_response), 'application/json')






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


class EstadosEndpoint(ProtectedResourceView):

    def get(self, request, *args, **kwargs):
        json_response = json.dumps(map(lambda estado: estado.to_serializable_dict(), Estado.objects.all()))
        return HttpResponse(json_response,'application/json')



class DependenciasEndpoint(ProtectedResourceView):

    def get(self, request):
        token = request.GET.get('access_token')
        print '*************' + token
        token_model = AccessToken.objects.get(token=token)
        print token_model.user

        if token_model.user.usuario.rol == 'SA':
            dicts = map(lambda dependencia: model_to_dict(dependencia), Dependencia.objects.all())

        elif token_model.user.usuario.rol == 'AD':
            dicts = map(lambda dependencia: model_to_dict(dependencia), Dependencia.objects.filter(
                Q(id=token_model.user.usuario.dependencia.id) |
                Q(dependienteDe__id=token_model.user.usuario.dependencia.id))
            )

        else:
            dicts = map(lambda dependencia: model_to_dict(dependencia), Dependencia.objects.filter(
                Q(id=token_model.user.usuario.dependencia.id))
            )

        for dictionary in dicts:
            # We KNOW that this entry must be a FileField value
            # (therefore, calling its name attribute is safe),
            # so we need to mame it JSON serializable (Django objects
            # are not by default and its built-in serializer sucks),
            # namely, we only need the path
            if dictionary['imagenDependencia'].name == '' or dictionary['imagenDependencia'].name == '':
                dictionary['imagenDependencia'] = None
            else:
                dictionary['imagenDependencia'] = dictionary['imagenDependencia'].name

        json_response = json.dumps(dicts)
        return HttpResponse(json_response, 'application/json')


class ImpactosEndpoint(ProtectedResourceView):

    def get(self, request):
        json_response = json.dumps(map(lambda impacto: model_to_dict(impacto), Impacto.objects.all()))
        return HttpResponse(json_response, 'application/json')


class InauguradorEndpoint(ProtectedResourceView):

    def get(self, request):
        json_response = json.dumps(map(lambda inaugurador: model_to_dict(inaugurador), Inaugurador.objects.all()))
        return HttpResponse(json_response, 'application/json')


class ClasificacionEndpoint(ProtectedResourceView):

    def get(self, request):
        if request.GET.get('id', False):
            clasificaciones = TipoClasificacion.objects.filter(subclasificacionDe_id=1)
        else:
            clasificaciones = TipoClasificacion.objects.filter(subclasificacionDe_id__isnull=True)

        json_response = json.dumps(map(lambda clasificacion: clasificacion.to_serializable_dict(), clasificaciones))
        return HttpResponse(json_response, 'application/json')


class InversionEndpoint(ProtectedResourceView):

    def get(self, request):
        json_response = json.dumps(map(lambda inversion: inversion.to_serializable_dict(), TipoInversion.objects.all()))
        return HttpResponse(json_response, 'application/json')


class TipoDeObraEndpoint(ProtectedResourceView):

    def get(self, request):
        json_response = json.dumps(map(lambda tipo: tipo.to_serializable_dict(), TipoObra.objects.all()))
        return HttpResponse(json_response, 'application/json')

class BuscadorEndpoint(ProtectedResourceView):

    def get(self, request):
        buscador = BuscarObras(idtipoobra=get_array_or_none(request.GET.get('tipoDeObra')),
                           iddependencias=get_array_or_none(request.GET.get('tipoDeObra')),
                           estados=get_array_or_none(request.GET.get('tipoDeObra')),
                           clasificaciones=get_array_or_none(request.GET.get('tipoDeObra')),
                           inversiones=get_array_or_none(request.GET.get('tipoDeObra')),
                           inauguradores=get_array_or_none(request.GET.get('tipoDeObra')),
                           impactos=get_array_or_none(request.GET.get('tipoDeObra')),
                           inaugurada=None,
                           inversion_minima=None,
                           inversion_maxima=None,
                           fecha_inicio_primera=None,
                           fecha_inicio_segunda=None,
                           fecha_fin_primera=None,
                           fecha_fin_segunda=None,
                           denominacion=None,
        )
        resultados = buscador.buscar()

        json_map = {}

        json_map['reporte_dependencia'] = []
        for reporte in resultados['reporte_dependencia']:
            map = {}
            map['dependencia'] = Dependencia.objects.get(nombreDependencia=reporte['dependencia__nombreDependencia']).to_serializable_dict()
            map['numero_obras'] = reporte['numero_obras']
            if reporte['sumatotal'] is None:
                map['sumatotal'] = 0
            else:
                map['sumatotal'] = int(reporte['sumatotal'])
            json_map['reporte_dependencia'].append(map)

        json_map['obras'] = []
        for obra in resultados['obras']:
            map = {}

            map['identificador'] = obra.identificador_unico
            map['tipoObra'] = obra.tipoObra.to_serializable_dict()
            map['dependencia'] = obra.dependencia.to_serializable_dict()
            map['estado'] = obra.estado.to_serializable_dict()
            map['impacto'] = obra.impacto.to_serializable_dict()

            map['tipoInversion'] = []
            for tipoInversion in obra.tipoInversion.all():
                tipo = tipoInversion.to_serializable_dict()
                map['tipoInversion'].append(tipo)

            map['tipoClasificacion'] = []
            for tipoClasificacion in obra.tipoClasificacion.all():
                tipo = tipoClasificacion.to_serializable_dict()
                map['tipoClasificacion'].append(tipo)

            map['inaugurador'] = obra.inaugurador.to_serializable_dict()
            map['registroHacendario'] = obra.registroHacendario
            map['registroAuditoria'] = obra.registroAuditoria
            map['denominacion'] = obra.denominacion
            map['descripcion'] = obra.descripcion
            map['observaciones'] = obra.observaciones
            if obra.fechaInicio is None:
                map['fechaInicio'] = None
            else:
                map['fechaInicio'] = obra.fechaInicio.__str__()
            if obra.fechaTermino is None:
                map['fechaTermino'] = None
            else:
                map['fechaTermino'] = obra.fechaTermino.__str__()
            if obra.inversionTotal is None:
                map['inversionTotal'] = 0.0
            else:
                map['inversionTotal'] = float(obra.inversionTotal)
            if obra.totalBeneficiarios is None:
                map['totalBeneficiarios'] = 0
            else:
                map['totalBeneficiarios'] = int(obra.totalBeneficiarios)
            map['senalizacion'] = obra.senalizacion
            map['susceptibleInauguracion'] = obra.susceptibleInauguracion
            if obra.porcentajeAvance is None:
                map['porcentajeAvance'] = 0.0
            else:
                map['porcentajeAvance'] = float(obra.porcentajeAvance)
            if obra.fotoAntes is None:
                map['fotoAntes'] = None
            else:
                map['fotoAntes'] = obra.fotoAntes.name
            if obra.fotoDurante is None:
                map['fotoAntes'] = None
            else:
                map['fotoAntes'] = obra.fotoDurante.name
            if obra.fotoDespues is None:
                map['fotoAntes'] = None
            else:
                map['fotoAntes'] = obra.fotoDespues.name
            map['inaugurada'] = obra.inaugurada
            map['poblacionObjetivo'] = obra.poblacionObjetivo
            map['municipio'] = obra.municipio
            if obra.tipoMoneda is None:
                map['tipoMoneda'] = None
            else:
                map['tipoMoneda'] = obra.tipoMoneda.to_serializable_dict()

            json_map['obras'].append(map)

        json_map['reporte_estado'] = []
        for reporte_estado in resultados['reporte_estado']:
            map = {}
            if reporte_estado['sumatotal'] is None:
                map['sumatotal'] = 0.0
            else:
                map['sumatotal'] = float(reporte_estado['sumatotal'])
            map['estado'] = Estado.objects.get(nombreEstado=reporte_estado['estado__nombreEstado']).to_serializable_dict()
            map['numeroObras'] = reporte_estado['numero_obras']

            json_map['reporte_estado'].append(map)

        json_map['reporte_general'] = []
        map = {}
        total = resultados['reporte_general']['total_invertido']['inversionTotal__sum']
        if total is None:
            total = 0.0
        else:
            total = float(total)
        map['total_invertido'] = total

        map['obras_totales'] = resultados['reporte_general']['obras_totales']
        json_map['reporte_general'].append(map)

        return HttpResponse(json.dumps(json_map), 'application/json')


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
    template = loader.get_template('consultas/busqueda_general.html')
    context = RequestContext(request, {
        'dependencias': dependencias,
        'estados': Estado.objects.all(),
        'tipo_inversiones': TipoInversion.objects.all(),
        'impactos': Impacto.objects.all(),
        'clasificacion': TipoClasificacion.objects.all(),
        'inaugurador': Inaugurador.objects.all(),
    })
    return HttpResponse(template.render(context))


def get_array_or_none(the_string):
    if the_string is None:
        return None
    else:
        return map(int, the_string.split(','))

def buscar_obras_web(request):
    #TODO cambiar los parametros 'None' por get del request
    buscador = BuscarObras(idtipoobra=get_array_or_none(request.GET.get('tipoDeObra')),
                           iddependencias=get_array_or_none(request.GET.get('tipoDeObra')),
                           estados=get_array_or_none(request.GET.get('tipoDeObra')),
                           clasificaciones=get_array_or_none(request.GET.get('tipoDeObra')),
                           inversiones=get_array_or_none(request.GET.get('tipoDeObra')),
                           inauguradores=get_array_or_none(request.GET.get('tipoDeObra')),
                           impactos=get_array_or_none(request.GET.get('tipoDeObra')),
                           inaugurada=None,
                           inversion_minima=None,
                           inversion_maxima=None,
                           fecha_inicio_primera=None,
                           fecha_inicio_segunda=None,
                           fecha_fin_primera=None,
                           fecha_fin_segunda=None,
                           denominacion=None,
    )
    resultados = buscador.buscar()

    template = loader.get_template('consultas/resultado_busqueda.html')
    context = RequestContext(request, {
        'resultados': resultados
    })
    return HttpResponse(template.render(context))


def ajax_prueba(request):
    template = loader.get_template('prueba.html')
    return HttpResponse(template.render(RequestContext(request)))