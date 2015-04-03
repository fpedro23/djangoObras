# Create your views here.
import datetime
import json
from obras.models import *
from oauth2_provider.views.generic import ProtectedResourceView
from django.db import connection, models
from django.forms.models import model_to_dict
from sp_models import *
from django.http import HttpResponse
from django.db.models import Q


class BusquedaEndpoint(ProtectedResourceView):

    def get(self, request):
        search_args = (request.GET.get('tipoDeObra', None), request.GET.get('dependencia', None),
                       request.GET.get('tipoDeObra', None), request.GET.get('estado', None),
                       request.GET.get('inversionMinima', None), request.GET.get('inversionMaxima', None),
                       request.GET.get('fechaInicio', None), request.GET.get('fechaInicioSegunda', None),
                       request.GET.get('fechaFin', None), request.GET.get('fechaFinSegunda', None),
                       request.GET.get('impacto', None), request.GET.get('inaugurador', None),
                       request.GET.get('tipoDeInversion', None), request.GET.get('clasificacion', None),
                       request.GET.get('susceptible', None), request.GET.get('inaugurada', None),
                       request.GET.get('limiteMin', None), request.GET.get('limiteMax', None),
                       request.GET.get('denominacion', None), request.GET.get('subclasificacion', None),
                       request.GET.get('subclasificacion', None), request.GET.get('subclasificacion', None), 15.0)

        cursor = connection.cursor()
        try:
            # { listaObras: [], listaReporteDependencia: [], listaReporteEstado: [] }
            # Call the stored procedure
            cursor.callproc('buscarObras', search_args)

            # listaObras
            listaObras = get_search_result_map(cursor.fetchall())

            # listaReporteDependencia
            cursor.nextset()
            listaReporteDependencia = get_dependency_report(cursor.fetchall())

            # listaReporteEstado
            cursor.nextset()
            # listaReporteEstado = get_state_report(cursor.fetchall())
            #
            # return create_full_report(listaObras, listaReporteDependencia, listaReporteEstado)
        except():
            return None

        finally:
            cursor.close()


class EstadosEndpoint(ProtectedResourceView):

    def get(self, request):
        json_response = json.dumps(map(lambda estado: model_to_dict(estado), Estado.objects.all()))
        return HttpResponse(json_response, 'application/json')


class DependenciasEndpoint(ProtectedResourceView):

    def get(self, request):
        dicts = map(lambda dependencia: model_to_dict(dependencia), Dependencia.objects.all())

        for dict in dicts:
            # We KNOW that this entry must be a FileField value
            # (therefore, calling its name attribute is safe),
            # so we need to mame it JSON serializable (Django objects
            # are not by default and its built-in serializer sucks),
            # namely, we only need the path
            if dict['imagenDependencia'].name == '' or dict['imagenDependencia'].name == '':
                dict['imagenDependencia'] = None
            else:
                dict['imagenDependencia'] = dict['imagenDependencia'].name

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

        json_response = json.dumps(map(lambda clasificacion: model_to_dict(clasificacion), clasificaciones))
        return HttpResponse(json_response, 'application/json')



class InversionEndpoint(ProtectedResourceView):

    def get(self, request):
        json_response = json.dumps(map(lambda inversion: model_to_dict(inversion), TipoInversion.objects.all()))
        return HttpResponse(json_response, 'application/json')


class TipoDeObraEndpoint(ProtectedResourceView):

    def get(self, request):
        json_response = json.dumps(map(lambda x: model_to_dict(x), TipoObra.objects.all()))
        return HttpResponse(json_response, 'application/json')


def index(request):
    data = "Respuesta = " + request.GET.get('id')
    return HttpResponse(data)


def balance_general(request):
    start_date = datetime.date(2012, 12, 01)
    end_date = datetime.date(2013, 12, 31)
    Obra.objects.filter(
        Q(fechaTermino__range=(start_date, end_date)),
        Q(tipoObra=3)
    )
