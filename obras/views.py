# Create your views here.
from obras.models import *
from oauth2_provider.views.generic import ProtectedResourceView
from django.db import connection
from sp_models import *


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
            listaReporteEstado = get_state_report(cursor.fetchall())

            return create_full_report(listaObras, listaReporteDependencia, listaReporteEstado)
        except():
            return None

        finally:
            cursor.close()import datetime

from django.http import HttpResponse
from django.db.models import Q

from obras.models import *


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